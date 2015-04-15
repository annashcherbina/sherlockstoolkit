class KinshipsController < ApplicationController
  before_action :set_kinship, only: [:show, :edit, :update, :destroy]

  # GET /kinships
  # GET /kinships.json
  def index
    @kinships = Kinship.all
  end

  # GET /kinships/1
  # GET /kinships/1.json
  def show
  end

  # GET /kinships/new
  def new
    @kinship = Kinship.new
  end

  # GET /kinships/1/edit
  def edit
  end

  # POST /kinships
  # POST /kinships.json
  def create
    @kinship = Kinship.new(kinship_params)

    respond_to do |format|
      if @kinship.save
        format.html { redirect_to @kinship, notice: 'Kinship was successfully created.' }
        format.json { render action: 'show', status: :created, location: @kinship }
      else
        format.html { render action: 'new' }
        format.json { render json: @kinship.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /kinships/1
  # PATCH/PUT /kinships/1.json
  def update
    respond_to do |format|
      if @kinship.update(kinship_params)
        format.html { redirect_to @kinship, notice: 'Kinship was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @kinship.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /kinships/1
  # DELETE /kinships/1.json
  def destroy
    @kinship.destroy
    respond_to do |format|
      format.html { redirect_to kinships_url }
      format.json { head :no_content }
    end
  end

  private
  # Use callbacks to share common setup or constraints between actions.
  def set_kinship
    @kinship = Kinship.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def kinship_params
    params.require(:kinship).permit(:relationship_id, :common_minor_alleles, :total_minor_alleles)
  end
end
