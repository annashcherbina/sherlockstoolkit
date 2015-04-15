class PrimersController < ApplicationController
  before_action :set_primer, only: [:show, :edit, :update, :destroy]

  # GET /primers
  # GET /primers.json
  def index
    if params[:panel_id] && Panel.exists?(params[:panel_id])
      @primers = Panel.find(params[:panel_id]).primers
    else
      @primers = Primer.all
    end
    @loci_hash = Tools::to_hash(Locus.all)
  end

  # GET /primers/1
  # GET /primers/1.json
  def show
  end

  # GET /primers/new
  def new
    @primer = Primer.new
  end

  # GET /primers/1/edit
  def edit
  end

  # POST /primers
  # POST /primers.json
  def create
    @primer = Primer.new(primer_params)

    respond_to do |format|
      if @primer.save
        format.html { redirect_to @primer, notice: 'Primer was successfully created.' }
        format.json { render action: 'show', status: :created, location: @primer }
      else
        format.html { render action: 'new' }
        format.json { render json: @primer.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /primers/1
  # PATCH/PUT /primers/1.json
  def update
    respond_to do |format|
      if @primer.update(primer_params)
        format.html { redirect_to @primer, notice: 'Primer was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @primer.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /primers/1
  # DELETE /primers/1.json
  def destroy
    @primer.destroy
    respond_to do |format|
      format.html { redirect_to primers_url }
      format.json { head :no_content }
    end
  end

  private
  # Use callbacks to share common setup or constraints between actions.
  def set_primer
    @primer = Primer.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def primer_params
    params.require(:primer).permit(:panel_id, :locus_id, :name, :is_forward, :sequence)
  end
end
