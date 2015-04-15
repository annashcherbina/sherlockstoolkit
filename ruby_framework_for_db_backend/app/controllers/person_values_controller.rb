class PersonValuesController < ApplicationController
  before_action :set_person_value, only: [:show, :edit, :update, :destroy]

  # GET /person_values
  # GET /person_values.json
  def index
    @person_values = PersonValue.all
  end

  # GET /person_values/1
  # GET /person_values/1.json
  def show
  end

  # GET /person_values/new
  def new
    @person_value = PersonValue.new
  end

  # GET /person_values/1/edit
  def edit
  end

  # POST /person_values
  # POST /person_values.json
  def create
    @person_value = PersonValue.new(person_value_params)

    respond_to do |format|
      if @person_value.save
        format.html { redirect_to @person_value, notice: 'Person value was successfully created.' }
        format.json { render action: 'show', status: :created, location: @person_value }
      else
        format.html { render action: 'new' }
        format.json { render json: @person_value.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /person_values/1
  # PATCH/PUT /person_values/1.json
  def update
    respond_to do |format|
      if @person_value.update(person_value_params)
        format.html { redirect_to @person_value, notice: 'Person value was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @person_value.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /person_values/1
  # DELETE /person_values/1.json
  def destroy
    @person_value.destroy
    respond_to do |format|
      format.html { redirect_to person_values_url }
      format.json { head :no_content }
    end
  end

  private
  # Use callbacks to share common setup or constraints between actions.
  def set_person_value
    @person_value = PersonValue.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def person_value_params
    params.require(:person_value).permit(:person_id, :attribute_id, :choice_id, :attribute_type, :attribute_int, :attribute_float, :attribute_string, :attribute_bool, :source, :is_truth)
  end
end
