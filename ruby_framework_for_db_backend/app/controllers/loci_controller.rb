class LociController < ApplicationController
  before_action :set_locus, only: [:show, :edit, :update, :destroy]

  # GET /loci
  # GET /loci.json
  def index
    if params[:panel_id] && Panel.exists?(params[:panel_id])
      @loci = Panel.find(params[:panel_id]).loci
    else
      @loci = Locus.all
    end
  end

  # GET /loci/1
  # GET /loci/1.json
  def show
  end

  # GET /loci/new
  def new
    @locus = Locus.new
  end

  # GET /loci/1/edit
  def edit
  end

  # POST /loci
  # POST /loci.json
  def create
    @locus = Locus.new(locus_params)

    respond_to do |format|
      if @locus.save
        format.html { redirect_to @locus, notice: 'Locus was successfully created.' }
        format.json { render action: 'show', status: :created, location: @locus }
      else
        format.html { render action: 'new' }
        format.json { render json: @locus.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /loci/1
  # PATCH/PUT /loci/1.json
  def update
    respond_to do |format|
      if @locus.update(locus_params)
        format.html { redirect_to @locus, notice: 'Locus was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @locus.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /loci/1
  # DELETE /loci/1.json
  def destroy
    @locus.destroy
    respond_to do |format|
      format.html { redirect_to loci_url }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_locus
      @locus = Locus.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def locus_params
      params.require(:locus).permit(:name, :locus_type, :chromosome, :region, :position, :exclude, :str_unit, :flank5, :snp_iub, :flank3)
    end
end
