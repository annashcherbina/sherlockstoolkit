class ExperimentsController < ApplicationController
  before_action :set_experiment, only: [:show, :edit, :update, :destroy]
  # GET /experiments
  # GET /experiments.json
  def index
    @experiments = Experiment.all
    @instruments = Instrument.all
    @instruments_hash = Tools::to_hash(@instruments)
    @panels = Panel.all
    @panels_hash = Tools::to_hash(@panels)
  end

  def form_action
    case params[:form_action]
      when 'Run Mixture Analysis'
        execute_mixture_analysis
      when 'Update/Create Parameter Group'
        execute_parameter_update
      else
        flash[:notice] = 'Unknown Button Pressed'
        redirect_to(:back)
    end
  end

# index

# GET /experiments/1
# GET /experiments/1.json
  def show
    @experiments_hash = Tools::to_hash(Experiment.all)
    @people_hash = Tools::to_hash(Person.all)
    @user_hash= Hash[User.pluck(:id, :username)]
    system_user_id = User.find_by_name('SYSTEM')
    @system_params = Parameter.where(user_id: system_user_id, group_name: 'System Defaults')

    #gon.parameters is accessible in javascript
    gon.parameters = Parameter.get_all_latest
  end

# show

# GET /experiments/new
  def new
    @experiment = Experiment.new
    @instruments = Instrument.all
    @folders = Folder.all
  end

# new

# GET /experiments/1/edit
  def edit
    @instruments = Instrument.all
    @folders = Folder.all
  end

# edit

# POST /experiments
# POST /experiments.json
  def create
    hash_name = params[:experiment][:datafile].original_filename.split('_')[0]
    @experiment = Experiment.find_by_hash_name(hash_name)

    respond_to do |format|
      if !@experiment.nil? && @experiment.update(experiment_params)
        format.html { redirect_to @experiment, notice: 'Experiment was successfully created.' }
        format.json { render action: 'show', status: :created, location: @experiment }
      else
        @instruments = Instrument.all
        @folders = Folder.all
        format.html { render action: 'new' }
        format.json { render json: @experiment.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /experiments/1
  # PATCH/PUT /experiments/1.json
  def update
    respond_to do |format|
      if @experiment.update(experiment_params)
        format.html { redirect_to @experiment, notice: 'Experiment was successfully updated.' }
        format.json { head :no_content }
      else
        @instruments = Instrument.all
        @folders = Folder.all
        format.html { render action: 'edit' }
        format.json { render json: @experiment.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /experiments/1
  # DELETE /experiments/1.json
  def destroy
    @experiment.destroy
    respond_to do |format|
      format.html { redirect_to experiments_url }
      format.json { head :no_content }
    end
  end

  private
  #Use callbacks to share common setup or constraints between actions.
  def set_experiment
    @experiment = Experiment.find(params[:id])
  end

  #Never trust parameters from the scary internet, only allow the white list through.
  def experiment_params
    params.require(:experiment).permit(:instrument_id, :primer_panel_id, :hash_name, :name, :is_mixture, :call_url,
                                       :final_lib_reads, :wells_with_isp, :live_isp, :filtered_polyclonal, :pcr,
                                       :amp_lig_quant, :empcr_date, :template_amount_loaded, :notes, :run_date, :datafile)
  end

  def execute_mixture_analysis
    #makes sure there are mixtures selected
    if params[:sample_cb].nil?
      flash[:notice] = 'Nothing selected!'
      redirect_to(:back)
      return
    end

    #assembles the various parameters for the mixture analysis call
    db_config = Rails.configuration.database_configuration[Rails.env]
    database = db_config['database']
    username = db_config['username']
    password = db_config['password']
    host = db_config['host']

    code_folder = (Rails.env == 'production' ? '/usr/local/mitll/production_backend' : '/usr/local/mitll/dev_backend')
    selected_param_group = params['Param Group']
    selected_locus_group_id = params['Selected Locus Group']

    mixture_quality = params['Mixture Quality']
    reference_quality = params['Reference Quality']
    sample_args = params[:sample_cb].keys.join(' ')
    folder_id = Folder.where(name: 'Mixture', level: 1).first.id

    python_cmd = "python #{code_folder}/mixture_2.0/truthMAF_db_barcode_person_input.py"\
    " -h #{host} -db #{database} -u #{username} -p #{password}"\
    " -removeBadSnps -mix #{sample_args} -qual_mix #{mixture_quality} -qual_ref #{reference_quality}"\
    " -parameter_group '#{selected_param_group}' -locus_group #{selected_locus_group_id}"\
    " -id_folder #{folder_id} -id_user #{session[:user_id]} -id_exp #{params[:id]}"

    python_response = `#{python_cmd}`

    #the last line of output from anna's mixture code is either a list of 4 comma separated numbers like 4,2,6,7
    #with the first four corresponding to image ids, the next two correspond to attachment ids produced by her code
    #if it is an error, it is in the format of a negative number followed by the error message
    last_line = python_response.strip.split(/\n/).last
    last_line ||= ''
    image_id = last_line.slice!(/-?\d+/).to_i

    #redirects to the image if it exists
    if Image.exists?(image_id)
      redirect_to(image_path(image_id))
      return
    elsif $?.exitstatus.zero?
      flash[:notice] = "Error:#{last_line}"
    else
      flash[:notice] = "Unhandled Exception, please send this to the admins: \"#{python_cmd}\""
    end

    #otherwise redirect back to where we were
    redirect_to(:back)
  end


  def execute_parameter_update
    #sends off the arguments to be processed, valid parameters to be created,
    # invalid ones ignored, with a new parameter group name if applicable
    param_update_args = {}
    param_update_args[:old_exp_params] = params[:old_exp_params]
    param_update_args[:new_exp_params] = params[:new_exp_params]
    param_update_args[:param_owner] = params['Param Owner'].to_i
    param_update_args[:param_group] = params['Param Group']
    param_update_args[:new_group_name] = params['New Group Name']

    parameter_response = Parameter.update_and_create_groups(session[:user_id], session[:username], param_update_args).html_safe

    flash[:notice] = parameter_response
    redirect_to :back
  end
end
