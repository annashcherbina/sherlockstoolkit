class EthnicitiesController < ApplicationController
  #before_action :set_ethnicity, only: [:show, :edit, :update, :destroy]

  # GET /ethnicities
  # GET /ethnicities.json
  def index
    @ethnicities = Ethnicity.all

    eth_array = []
    @ethnicities.each do |ethnicity|
      next if ethnicity.name == 'global'
      eth_array << DataMapBubble.new(1, 5, 5, ethnicity.name, '1', ethnicity.lat, ethnicity.lng).to_json
    end

    @all_ethnicities = '[' + eth_array.join(',') + ']'
  end
=begin
  # GET /ethnicities/1
  # GET /ethnicities/1.json
  def show
  end

  # GET /ethnicities/new
  def new
    @ethnicity = Ethnicity.new
  end

  # GET /ethnicities/1/edit
  def edit
  end

  # POST /ethnicities
  # POST /ethnicities.json
  def create
    @ethnicity = Ethnicity.new(ethnicity_params)

    respond_to do |format|
      if @ethnicity.save
        format.html { redirect_to @ethnicity, notice: 'Ethnicity was successfully created.' }
        format.json { render action: 'show', status: :created, location: @ethnicity }
      else
        format.html { render action: 'new' }
        format.json { render json: @ethnicity.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /ethnicities/1
  # PATCH/PUT /ethnicities/1.json
  def update
    respond_to do |format|
      if @ethnicity.update(ethnicity_params)
        format.html { redirect_to @ethnicity, notice: 'Ethnicity was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @ethnicity.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /ethnicities/1
  # DELETE /ethnicities/1.json
  def destroy
    @ethnicity.destroy
    respond_to do |format|
      format.html { redirect_to ethnicities_url }
      format.json { head :no_content }
    end
  end

  private
  # Use callbacks to share common setup or constraints between actions.
  def set_ethnicity
    @ethnicity = Ethnicity.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def ethnicity_params
    params.require(:ethnicity).permit(:name, :race)
  end
=end
end
