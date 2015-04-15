class SamplesController < ApplicationController
  before_action :set_sample, only: [:show, :edit, :update, :destroy], except: [:form_action]

  # GET /samples
  # GET /samples.json
  def index
    @experiments_hash = Tools::to_hash(Experiment.all)
    @barcodes_hash = Tools::to_hash(Barcode.all)
    @samples_view_index_hash = Sample.make_samples_index_hash(@experiments_hash)
    @user_hash= Hash[User.pluck(:id, :username)]

    system_user_id = User.find_by_name('SYSTEM')
    @system_params = Parameter.where(user_id: system_user_id, group_name: 'System Defaults')

    #gon.parameters is accessible in javascript
    gon.parameters = Parameter.get_all_latest
  end

  #executes mixture,replicate, or ancestry code depending on which graph button was pressed in the samples controller
  def form_action
    #redirect back to index if there are no values selected and parameters are not being updated
    if params[:chosen_samples].nil? &&
        params[:form_action] != 'Update/Create Parameter Group' &&
        params[:form_action] != 'Total Reads by Experiment'
      flash[:notice] = 'Nothing selected!'
      redirect_to(:back)
      return
    end

    code_folder = (Rails.env == 'production' ? '/usr/local/mitll/production_backend' : '/usr/local/mitll/dev_backend')
    db_config = Rails.configuration.database_configuration[Rails.env]
    database = db_config['database']
    username = db_config['username']
    password = db_config['password']
    host = db_config['host']
    selected_param_group = params['Param Group']
    selected_locus_group = params['Locus Group']
    selected_quality = params['Sample Quality']

    python_args = " -h #{host} -db #{database} -u #{username} -p #{password}"\
    " -parameter_group '#{selected_param_group}' -locus_group #{selected_locus_group} -quality #{selected_quality}"\
    " -id_user #{session[:user_id]}"

    case params[:form_action]
      #replicate module call
      when 'Replicate'
        execute_replicate_analysis(code_folder, python_args)
      #ancestry module call
      when 'Ancestries'
        execute_ancestry_analysis(code_folder, python_args)
      when 'Quality Control'
        execute_qc(code_folder, python_args)
      when 'Total Reads by Experiment'
        execute_qc_reads(code_folder, python_args)
      #kinship module call
      when 'Kinship'
        execute_kinship_analysis(code_folder, python_args)
      #when 'Update Parameters/Create Parameter Group'
      when 'Update/Create Parameter Group'
        execute_parameter_update
      #default case, should never happen, but handle errors just in case
      else
        flash[:notice] = 'Unknown Button Pressed.'
        redirect_to(:back)
    end
  end

  # GET /samples/1
  # GET /samples/1.json
  def show
  end

  # GET /samples/new
  def new
    @sample = Sample.new
  end

  # GET /samples/1/edit
  def edit
  end

  # POST /samples
  # POST /samples.json
  def create
    @sample = Sample.new(sample_params)

    respond_to do |format|
      if @sample.save
        format.html { redirect_to @sample, notice: 'Sample was successfully created.' }
        format.json { render action: 'show', status: :created, location: @sample }
      else
        format.html { render action: 'new' }
        format.json { render json: @sample.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /samples/1
  # PATCH/PUT /samples/1.json
  def update
    respond_to do |format|
      if @sample.update(sample_params)
        format.html { redirect_to @sample, notice: 'Sample was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @sample.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /samples/1
  # DELETE /samples/1.json
  def destroy
    @sample.destroy
    respond_to do |format|
      format.html { redirect_to samples_url }
      format.json { head :no_content }
    end
  end




  private
  # Use callbacks to share common setup or constraints between actions.
  def set_sample
    @sample = Sample.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def sample_params
    params.require(:sample).permit(:experiment_id, :barcode_id, :is_good, :is_mixture, :minor_alleles_called)
  end

  #parepares for calling the replicate code
  def execute_replicate_analysis(code_folder, python_args)
    #ensure that the user has selected samples
    unless params[:chosen_samples].present?
      flash[:notice] = 'Samples must be chosen on an individual person level in order to do a Replicate Analysis.'
      redirect_to(:back)
      return
    end

    folder_id = Folder.where(name: 'Replicate', level: 1).first.id
    #filters out what samples were selected by the user at replicate or truth levels
    sample_args = params[:replicate_samples_status].select{ |k, v| params[:chosen_samples].keys.include?(k) }
    #space separates the sample ids for replicate level and truth level (e.g. 52 55 172)
    replicate_args = sample_args.select { |key, value| value == 'Replicate' }.keys.map { |e| e.to_i }.join(' ')
    truth_args = sample_args.select { |key, value| value == 'Truth' }.keys.map { |e| e.to_i }.join(' ')

    #execute the code and then parse the response
    python_cmd = "python #{code_folder}/replicate_2.0/analyzeReplicates.py"\
    " –rep #{replicate_args} -truth #{truth_args}"\
    "#{python_args}"\
    " -id_folder #{folder_id}"

    python_response = `#{python_cmd}`

    samples_redirect_handler($?.exitstatus, python_response, python_cmd)
  end

  def execute_qc(code_folder, python_args)
    folder_id = Folder.find_by(name: 'Quality Control', level: 1).id
    sample_args = params[:chosen_samples].keys.join(' ')
    python_cmd = "python #{code_folder}/qc/qcSamples.py"\
    " -samples #{sample_args}"\
    "#{python_args}"\
    " -id_folder #{folder_id}"

    python_response = `#{python_cmd}`

    samples_redirect_handler($?.exitstatus, python_response, python_cmd)
  end

  def execute_qc_reads(code_folder, python_args)
    folder_id = Folder.find_by(name: 'Quality Control', level: 1).id
    python_cmd = "python #{code_folder}/readcounts/countReads.py"\
    "#{python_args}"\
    " –id_folder #{folder_id}"

    python_response = `#{python_cmd}`

    samples_redirect_handler($?.exitstatus, python_response, python_cmd)
  end

  #prepares for calling the ancestry code
  def execute_ancestry_analysis(code_folder, python_args)
    folder_id = Folder.where(name: 'Ancestry', level: 1).first.id
    #if a group is selected, go and find all the samples associated with that group
    sample_args = params[:chosen_samples].keys.join(' ')

    python_cmd = "python #{code_folder}/ancestry_2.0/ancestry_gen_alg.py"\
    " -samples #{sample_args}"\
    "#{python_args}"\
    " -id_folder #{folder_id}"

    python_response = `#{python_cmd}`

    if $?.exitstatus.zero?
      response_array = python_response.split(/\n/)
      ancestry_successes = response_array[-1].gsub(/[^0-9\s]/, '').split(' ')
      ancestry_failures = response_array[-2].gsub(/[^0-9\s]/, '').split(' ')
      attachment_id = response_array[-3][/\d+/]

      redirect_to(map_ancestries_path(attachment_id: attachment_id, successes: ancestry_successes, failures: ancestry_failures))
    else
      flash[:notice] = "Unhandled Exception, please send this to the admins: \"#{python_cmd}\""
      redirect_to(:back)
    end
  end

  #kinship module call
  def execute_kinship_analysis(code_folder, python_args)
    folder_id = Folder.where(name: 'Kinship', level: 1).first.id
    sample_args =  params[:chosen_samples].keys.join(' ')

    #assigning the Kinship Training Module Name depending on if the user selects it from dropdown or enters a new one in
    #also verifies the uniqueness of names before creation
    if params['Kinship Training Module'] == 'New Training Module'
      kinship_module = params['New Kinship Module Name']
      unless KinshipTrainingModule.pluck(:name).include?(kinship_module)
        KinshipTrainingModule.create(name: kinship_module)
      end
    else
      kinship_module = params['Kinship Training Module']
    end

    python_cmd = "python #{code_folder}/kinship_2.0/computeKinship.py"\
    " -samples #{sample_args}"\
    "#{python_args}"\
    " -training_module '#{kinship_module}'"\
    " -id_folder #{folder_id}"

    python_response = `#{python_cmd}`

    samples_redirect_handler($?.exitstatus, python_response, python_cmd)
  end

  #handles redirects for mixture, replicate, and qc modules based on the last line of the output of the python command where
  #the last line of the python_response is in the form of
  #a space separated series of numbers like "2 6 2 1" where they are attachment or image ids
  #or if it is an error, then the first number is negative and then followed by the error code such as "-1 Invalid Selection"
  def samples_redirect_handler(exit_code, python_response, python_cmd)
    #clears the params to save session cookie space
  params_cleanup

    #new flow control for handling exit status first, then checking if image exists
    if exit_code.zero?
      #grabs the last line of the std output of the module, which has the image id's, or an error code followed by a message
      last_line = python_response.strip.split(/\n/).last
      last_line ||= ''
      image_id = last_line.slice!(/-?\d+/).to_i

      if Image.exists?(image_id)
        redirect_to(image_path(image_id))
        return
      else
        flash[:notice] = "Error:#{last_line}"
      end
    else
      flash[:notice] = "Unhandled Exception, please send this to the admins: \"#{python_cmd}\""
    end

    #otherwise redirect back to where we were
    redirect_to(:back)
  end

  #creates new parameters that are valid, flash notices the ones that are not valid, returns to samples index
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
  #removes unnecessary params from being passed in order to avoid a cookie overflow
  def params_cleanup
    params.delete(:replicate_samples_status)
    params.delete(:chosen_samples)
    params.delete(:new_exp_params)
    params.delete(:old_exp_params)
  end
end
