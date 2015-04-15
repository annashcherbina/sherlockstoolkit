class LociGroupsController < ApplicationController
  before_action :set_loci_group, only: [:show, :edit, :update, :destroy]

  # GET /loci_groups
  # GET /loci_groups.json
  def index
    @loci_groups = LociGroup.all
  end

  # GET /loci_groups/1
  # GET /loci_groups/1.json
  def show
    @locus_names = @loci_group.loci.pluck(:name)
  end

  # GET /loci_groups/new
  def new
    @loci_group = LociGroup.new
  end

  # GET /loci_groups/1/edit
  def edit
  end

  # POST /loci_groups
  # POST /loci_groups.json
  def create
    #ensures a text file was attached
    unless params[:loci_group][:uploaded_file].present? && params[:loci_group][:uploaded_file].respond_to?(:read)
      flash[:notice] = 'Must have a text file of Loci'
      redirect_to :back
      return
    end

    loci_group_name = params[:loci_group][:name]
    @loci_group = LociGroup.new(name: loci_group_name)

    respond_to do |format|
      if @loci_group.save
        notice = "Locus Group created #{loci_group_name}"

        invalid_locus_names = LociGroup.create_group(@loci_group.id, params[:loci_group][:uploaded_file])
        notice.concat "<br />Error, these Loci could not be found: #{invalid_locus_names.to_a.join(', ')}" unless invalid_locus_names.empty?

        format.html { redirect_to @loci_group, notice: notice.html_safe }
        format.json { render action: 'show', status: :created, location: @loci_group }
      else
        format.html { render action: 'new' }
        format.json { render json: @loci_group.errors, status: :unprocessable_entity }
      end
    end
  end



  # PATCH/PUT /loci_groups/1
  # PATCH/PUT /loci_groups/1.json
  def update
    respond_to do |format|
      if @loci_group.update(loci_group_params)
        format.html { redirect_to @loci_group, notice: 'Loci group was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @loci_group.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /loci_groups/1
  # DELETE /loci_groups/1.json
  def destroy
    @loci_group.destroy
    respond_to do |format|
      format.html { redirect_to loci_groups_url }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_loci_group
      @loci_group = LociGroup.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def loci_group_params
      params.require(:loci_group).permit(:name)
    end
end
