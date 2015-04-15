class LocusAttributesController < ApplicationController
  before_action :set_locus_attribute, only: [:show, :edit, :update, :destroy]

  # GET /locus_attributes
  # GET /locus_attributes.json
  def index
    @locus_attributes = LocusAttribute.all
  end

  # GET /locus_attributes/1
  # GET /locus_attributes/1.json
  def show
  end

  # GET /locus_attributes/new
  def new
    @locus_attribute = LocusAttribute.new
  end

  # GET /locus_attributes/1/edit
  def edit
  end

  # POST /locus_attributes
  # POST /locus_attributes.json
  def create
    @locus_attribute = LocusAttribute.new(locus_attribute_params)

    respond_to do |format|
      if @locus_attribute.save
        format.html { redirect_to @locus_attribute, notice: 'Locus attribute was successfully created.' }
        format.json { render action: 'show', status: :created, location: @locus_attribute }
      else
        format.html { render action: 'new' }
        format.json { render json: @locus_attribute.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /locus_attributes/1
  # PATCH/PUT /locus_attributes/1.json
  def update
    respond_to do |format|
      if @locus_attribute.update(locus_attribute_params)
        format.html { redirect_to @locus_attribute, notice: 'Locus attribute was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @locus_attribute.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /locus_attributes/1
  # DELETE /locus_attributes/1.json
  def destroy
    @locus_attribute.destroy
    respond_to do |format|
      format.html { redirect_to locus_attributes_url }
      format.json { head :no_content }
    end
  end

  private
  # Use callbacks to share common setup or constraints between actions.
  def set_locus_attribute
    @locus_attribute = LocusAttribute.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def locus_attribute_params
    params.require(:locus_attribute).permit(:locus_id, :attribute_name, :attribute_choice)
  end
end
