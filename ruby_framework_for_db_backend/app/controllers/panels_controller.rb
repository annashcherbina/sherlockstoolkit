class PanelsController < ApplicationController
  before_action :set_panel, only: [:show, :edit, :update, :destroy]

  # GET /panels
  # GET /panels.json
  def index
    @panels = Panel.all
  end

  # GET /panels/1
  # GET /panels/1.json
  def show
  end

  # GET /panels/new
  def new
    @panel = Panel.new
  end

  # GET /panels/1/edit
  def edit
  end

  # POST /panels
  # POST /panels.json
  def create
    @panel = Panel.new(panel_params)
    respond_to do |format|
      if @panel.save
        attachment = Attachment.find(@panel.attachment_id)

        case @panel.panel_type
          when "Barcodes"
            BarcodeLoader::load_barcodes(attachment, @panel.id)
          when "Primers"
            PrimerLoader::load_primers(attachment, @panel.id)
          when "SNP References"
            LocusLoader::load_loci(attachment, @panel.id)
          else
            return
        end

        format.html { redirect_to @panel, notice: 'Panel was successfully created.' }
        format.json { render action: 'show', status: :created, location: @panel }
      else
        flash.now[:notice] = "Panel was not successfully created"
        format.html { render action: 'new' }
        format.json { render json: @panel.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /panels/1
  # PATCH/PUT /panels/1.json
  def update
    respond_to do |format|
      if @panel.update(panel_params)
        format.html { redirect_to @panel, notice: 'Panel was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @panel.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /panels/1
  # DELETE /panels/1.json
  def destroy

    # Drop all attachments for panel
    Attachment.destroy(@panel.attachment_id)

    Barcode.destroy(panel_id: @panel.id)
    Primer.destroy_all(panel_id: @panel.id)
    PanelLocus.destroy_all(panel_id: @panel.id)

    @panel.destroy
    respond do |format|
      format.html { redirect_to panels_url }
      format.json { head :no_content }
    end
  end

  private
  # Use callbacks to share common sep or constraints between actions.
  def set_panel
    @panel = Panel.find(params[:id])
  end

  # Never trust parameters om the ary internet, only allow the white list through.
  def panel_params
    params.require(:panel).permit(:name, :panel_type, :description, :updated_at, :attachment_id, :datafile)
  end
end
