class AncestriesController < ApplicationController
  before_action :set_ancestry, only: [:show, :edit, :update, :destroy]

  # GET /ancestries
  # GET /ancestries.json
  def index
    @ancestries = Ancestry.all
  end

  # GET /ancestries/1
  # GET /ancestries/1.json
  def show
  end

  # GET /ancestries/new
  def new
    @ancestry = Ancestry.new
  end

  # GET /ancestries/1/edit
  def edit
  end

  # POST /ancestries
  # POST /ancestries.json
  def create
    @ancestry = Ancestry.new(ancestry_params)

    respond_to do |format|
      if @ancestry.save
        format.html { redirect_to @ancestry, notice: 'Ancestry was successfully created.' }
        format.json { render action: 'show', status: :created, location: @ancestry }
      else
        format.html { render action: 'new' }
        format.json { render json: @ancestry.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /ancestries/1
  # PATCH/PUT /ancestries/1.json
  def update
    respond_to do |format|
      if @ancestry.update(ancestry_params)
        format.html { redirect_to @ancestry, notice: 'Ancestry was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @ancestry.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /ancestries/1
  # DELETE /ancestries/1.json
  def destroy
    @ancestry.destroy
    respond_to do |format|
      format.html { redirect_to ancestries_url }
      format.json { head :no_content }
    end
  end

  #takes in params[:successes] and params[:failures]
  #generates the D3 DataMap variables @datamap_bubbles, @datamap_fills, required to make a map
  #also the @successes and @failures hashes to display information to page
  def map
    #gets the parameters
    @parameters = {}
    if params[:attachment_id]
      attachment = Attachment.find(params[:attachment_id])
      attachment.parameters.map{ |parameter| @parameters[parameter.name]=parameter.value }
    end

    #creates a hash of PersonSamples to an ActiveRelation of their Ancestries
    people_samples_hash = Tools::to_hash(PersonSample.all)
    @ethnicity_hash = Tools::to_hash(Ethnicity.all)
    experiments_hash = Tools::to_hash(Experiment.all)
    samples_hash = Tools::to_hash(Sample.all)

    #in the event there are no successes or failures, just default to empty values
    params[:successes] ||= []
    params[:failures] ||= []

    #lists out the successes and failures in the form of person_id - experiment_name
    @successes = ps_ids_to_name_and_exp_name(params[:successes].map{ |e| e.to_i }, people_samples_hash, experiments_hash, samples_hash)
    @failures = ps_ids_to_name_and_exp_name(params[:failures].map{ |e| e.to_i }, people_samples_hash, experiments_hash, samples_hash)

    #handles what happens if @successes or @failures is empty
    handle_empty_ancestries(params, @failures)
    if flash[:notice]
      redirect_to(samples_path)
      return
    end

    #the hash used to convert the legend on the map to hyperlinks
    @legend_json = @successes.invert.to_json

    #the input, as an array of person_sample id's
    person_sample_ids = params[:successes].map{ |e| e.to_i }

    #ancestry must be of a certain percentage before they are mapped
    precentage_thresh = @parameters['Minimum ancestry contributions to report (percent)'] || 0.10
    #number of datamaps per person_sample
    ancestry_limit    = @parameters['Minimum ancestry contributions to report (integer)'].to_i || 1

    #creates a hash of persons identified by an experiment to their ancestries determined by that experiment
    @persons_ancestries_hash = {}

    person_sample_ids.each do |person_sample_id|
      @persons_ancestries_hash[@successes[person_sample_id]] =
      #the top $ANCESTRY_LIMIT ancestries for a person_sample that are above $PERCENTAGE_THRESH in descending order
          Ancestry.where(person_sample_id: person_sample_id).where("ancestries.percent > #{precentage_thresh}").order("ancestries.percent DESC").limit("#{ancestry_limit}")
    end

    #creates a sorted array of DataMapBubbles by likelihood in reverse order for all the PersonSamples
    bubbles_array = []
    @persons_ancestries_hash.each do |experiment_person, ancestries|
      ancestries.each do |ancestry|
        ethnicity = @ethnicity_hash[ancestry.ethnicity_id]
        bubbles_array << DataMapBubble.new(experiment_person, ancestry.percent, ancestry.percent, ethnicity.name, experiment_person, ethnicity.lat, ethnicity.lng)
      end
    end
    #ensures the smaller bubbles with smaller radii are displayed ontop of the bigger ones
    bubbles_array.sort_by!{ |dmb| -dmb.radius }

    #placing the data into a javascript readable string
    @datamap_bubbles = '[' + bubbles_array.map{ |e| e.to_json }.join(',') + ']'

    #creates a javascript readable string of color fills
    @datamap_fills = make_fills(@successes.values).to_json
  end #def map


  private
  # Use callbacks to share common setup or constraints between actions.
  def set_ancestry
    @ancestry = Ancestry.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def ancestry_params
    params.require(:ancestry).permit(:person_id, :ethnicity_id, :percent)
  end

  #creates the fills array required for the datamaps
  def make_fills(id_code_array)
    fills = {:defaultFill => 'silver'}
    #the set of used colors to ensure all colors in the fills hash is unique
    used_colors = Set.new ['#C0C0C0']
    #adds random colors to each id_code
    id_code_array.sort_by{ |elem| elem.to_i }.each do |id_code|
      color = ''
      #ensures random colors are unique
      while true
        color = '#%06x' % (rand * 0xffffff)
        break unless used_colors.add?(color).nil?
      end
      fills[id_code] = color
    end
    fills
  end

  #if there were person_samples with insufficient panel data to process their ancestries, sets a flash notice to alert the user
  #the output is in the form of a hash, where the key is the person_sample id, and the value is "PERSON ID CODE - EXPERIMENT NAME"
  def ps_ids_to_name_and_exp_name(ps_ids, people_samples_hash, experiments_hash, samples_hash)
    details = {}
    people_hash = Tools::to_hash(Person.all)
    ps_ids.each do |ps_id|
      details[ps_id] = "#{people_hash[people_samples_hash[ps_id].person_id].id_code} - #{experiments_hash[samples_hash[people_samples_hash[ps_id].sample_id].experiment_id].name}"
    end
    details
  end

  def handle_empty_ancestries(params, failures)
    #map module requires some person samples for which ancestries have been generated successfully
    if params[:successes].empty?
      if params[:failures].empty?
        flash[:notice] = 'No valid data to map.'
      else
        flash[:notice] = "Insufficient panel data for all samples chosen: #{failures.values.sort.join(', ')}. No ancestry data processed."
      end
    end
  end

end
