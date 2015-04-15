class SNPsController < ApplicationController
  before_action :set_snp, only: [:show, :edit, :update, :destroy]

  # GET /snps
  # GET /snps.json
  def index
    @snps = SNP.all
    @snps_hash = Tools::to_hash(@snps)
    @experiments_hash = Tools::to_hash(Experiment.all)
    @primers_hash = Tools::to_hash(Primer.all)
    @loci_hash = Tools::to_hash(Locus.all)
  end

  # GET /snps/1
  # GET /snps/1.json
  def show
  end

  # GET /snps/new
  def new
    @snp = SNP.new
  end

  # GET /snps/1/edit
  def edit
  end

  # POST /snps
  # POST /snps.json
  def create
    @snp = SNP.new(snp_params)

    respond_to do |format|
      if @snp.save
        format.html { redirect_to @snp, notice: 'SNP was successfully created.' }
        format.json { render action: 'show', status: :created, location: @snp }
      else
        format.html { render action: 'new' }
        format.json { render json: @snp.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /snps/1
  # PATCH/PUT /snps/1.json
  def update
    respond_to do |format|
      if @snp.update(snp_params)
        format.html { redirect_to @snp, notice: 'SNP was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @snp.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /snps/1
  # DELETE /snps/1.json
  def destroy
    @snp.destroy
    respond_to do |format|
      format.html { redirect_to snps_url }
      format.json { head :no_content }
    end
  end

  private
  # Use callbacks to share common setup or constraints between actions.
  def set_snp
    @snp = SNP.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def snp_params
    params.require(:snp).permit(:experiment_id, :primer_id, :locus_id, :sample_id, :allele_base, :count, :forward_qual, :reverse_qual, :is_minor, :flank5, :flank3)
  end
end
