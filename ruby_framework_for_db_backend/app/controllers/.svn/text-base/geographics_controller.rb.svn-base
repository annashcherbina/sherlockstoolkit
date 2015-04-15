class GeographicsController < ApplicationController
  before_action :set_geographic, only: [:show, :edit, :update, :destroy]

  # GET /geographics
  # GET /geographics.json
  def index
    @geographics = Geographic.all
  end

  # GET /geographics/1
  # GET /geographics/1.json
  def show
  end

  # GET /geographics/new
  def new
    @geographic = Geographic.new
  end

  # GET /geographics/1/edit
  def edit
  end

  # POST /geographics
  # POST /geographics.json
  def create
    @geographic = Geographic.new(geographic_params)

    respond_to do |format|
      if @geographic.save
        format.html { redirect_to @geographic, notice: 'Geographic was successfully created.' }
        format.json { render action: 'show', status: :created, location: @geographic }
      else
        format.html { render action: 'new' }
        format.json { render json: @geographic.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /geographics/1
  # PATCH/PUT /geographics/1.json
  def update
    respond_to do |format|
      if @geographic.update(geographic_params)
        format.html { redirect_to @geographic, notice: 'Geographic was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @geographic.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /geographics/1
  # DELETE /geographics/1.json
  def destroy
    @geographic.destroy
    respond_to do |format|
      format.html { redirect_to geographics_url }
      format.json { head :no_content }
    end
  end

  private
  # Use callbacks to share common setup or constraints between actions.
  def set_geographic
    @geographic = Geographic.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def geographic_params
    params.require(:geographic).permit(:region_name)
  end
end
