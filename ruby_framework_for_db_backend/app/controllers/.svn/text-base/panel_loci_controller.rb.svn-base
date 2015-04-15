class PanelLociController < ApplicationController
  before_action :set_panel_locus, only: [:show, :edit, :update, :destroy]

  # GET /panel_loci
  # GET /panel_loci.json
  def index
    @panel_loci = PanelLocus.all
    @panels_hash = Tools::to_hash(Panel.all)
    @locus_hash = Tools::to_hash(Locus.all)
  end

  # GET /panel_loci/1
  # GET /panel_loci/1.json
  def show
  end

  # GET /panel_loci/new
  def new
    @panel_locus = PanelLocus.new
  end

  # GET /panel_loci/1/edit
  def edit
  end

  # POST /panel_loci
  # POST /panel_loci.json
  def create
    @panel_locus = PanelLocus.new(panel_locus_params)

    respond_to do |format|
      if @panel_locus.save
        format.html { redirect_to @panel_locus, notice: 'Panel locus was successfully created.' }
        format.json { render action: 'show', status: :created, location: @panel_locus }
      else
        format.html { render action: 'new' }
        format.json { render json: @panel_locus.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /panel_loci/1
  # PATCH/PUT /panel_loci/1.json
  def update
    respond_to do |format|
      if @panel_locus.update(panel_locus_params)
        format.html { redirect_to @panel_locus, notice: 'Panel locus was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @panel_locus.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /panel_loci/1
  # DELETE /panel_loci/1.json
  def destroy
    @panel_locus.destroy
    respond_to do |format|
      format.html { redirect_to panel_loci_url }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_panel_locus
      @panel_locus = PanelLocus.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def panel_locus_params
      params.require(:panel_locus).permit(:panel_id, :locus_id, :exclude, :ambiguous, :low, :strand_bias)
    end
end
