class AlleleReferencesController < ApplicationController
  before_action :set_allele_reference, only: [:show, :edit, :update, :destroy]

  # GET /allele_references
  # GET /allele_references.json
  def index
    @allele_references = AlleleReference.all
  end

  # GET /allele_references/1
  # GET /allele_references/1.json
  def show
  end

  # GET /allele_references/new
  def new
    @allele_reference = AlleleReference.new
  end

  # GET /allele_references/1/edit
  def edit
  end

  # POST /allele_references
  # POST /allele_references.json
  def create
    @allele_reference = AlleleReference.new(allele_reference_params)

    respond_to do |format|
      if @allele_reference.save
        format.html { redirect_to @allele_reference, notice: 'Allele reference was successfully created.' }
        format.json { render action: 'show', status: :created, location: @allele_reference }
      else
        format.html { render action: 'new' }
        format.json { render json: @allele_reference.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /allele_references/1
  # PATCH/PUT /allele_references/1.json
  def update
    respond_to do |format|
      if @allele_reference.update(allele_reference_params)
        format.html { redirect_to @allele_reference, notice: 'Allele reference was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @allele_reference.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /allele_references/1
  # DELETE /allele_references/1.json
  def destroy
    @allele_reference.destroy
    respond_to do |format|
      format.html { redirect_to allele_references_url }
      format.json { head :no_content }
    end
  end

  private
  # Use callbacks to share common setup or constraints between actions.
  def set_allele_reference
    @allele_reference = AlleleReference.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def allele_reference_params
    params.require(:allele_reference).permit(:locus_id, :allele_name, :regular_expression, :allele_sequence)
  end
end
