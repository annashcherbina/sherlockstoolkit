class ParametersController < ApplicationController
  before_action :set_parameter, only: [:show, :edit, :update, :destroy]

  # GET /parameters
  # GET /parameters.json
  def index
    @users_hash = Tools::to_hash(User.all)

    #the number of unique parameter names to be displayed per page
    gon.unique_param_names = Parameter.uniq.pluck(:name).size

    #gets the latest parameters in the form of a parameters{} hash in the form of
    #parameters[$USER_ID][$GROUP_NAME] = $PARAMETER
    parameters_nested_hash = {}
    params_hash = Tools::to_hash(Parameter.all).sort
    params_hash.each do |param_id, parameter|
      parameters_nested_hash[parameter.user_id] ||= {}
      parameters_nested_hash[parameter.user_id][parameter.group_name] ||= {}
      parameters_nested_hash[parameter.user_id][parameter.group_name][parameter.name] = parameter
    end

    @parameters_array = []
    parameters_nested_hash.each{
        |owner_key, group_key| group_key.each{
          |group, name_key| name_key.each{
            |name, parameter| @parameters_array << parameter}
      }
    }
  end

  # GET /parameters/1
  # GET /parameters/1.json
  def show
  end

  # GET /parameters/new
  def new
    @parameters = Parameter.get_all_groups
  end

  # GET /parameters/1/edit
  def edit
  end

  # POST /parameters
  # POST /parameters.json
  def create
    @parameter = Parameter.new(parameter_params)

    respond_to do |format|
      if @parameter.save
        format.html { redirect_to @parameter, notice: 'Parameter was successfully created.' }
        format.json { render action: 'show', status: :created, location: @parameter }
      else
        format.html { render action: 'new' }
        format.json { render json: @parameter.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /parameters/1
  # PATCH/PUT /parameters/1.json
  def update
    respond_to do |format|
      if @parameter.update(parameter_params)
        format.html { redirect_to @parameter, notice: 'Parameter was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @parameter.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /parameters/1
  # DELETE /parameters/1.json
  def destroy
    @parameter.destroy
    respond_to do |format|
      format.html { redirect_to parameters_url }
      format.json { head :no_content }
    end
  end

  private
  # Use callbacks to share common setup or constraints between actions.
  def set_parameter
    @parameter = Parameter.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def parameter_params
    params.require(:parameter).permit(:user_id, :category, :name, :value)
  end
end
