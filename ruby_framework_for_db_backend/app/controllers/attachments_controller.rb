class AttachmentsController < ApplicationController
  before_action :set_attachment, only: [:show, :edit, :update, :destroy, :download]

  # GET /attachments
  # GET /attachments.json
  def index
    if params[:folder_id]
      @attachments = Folder.find(params[:folder_id]).attachments
    else
      @attachments = Attachment.all
    end
    @users_hash = Tools::to_hash(User.all)
    @folders_hash = Tools::to_hash(Folder.all)
  end

  # GET /attachments/1
  # GET /attachments/1.json
  def show
    @folder = Folder.find_by_id(params[:folder_id]) if params[:folder_id]
  end

  # GET /attachments/new
  def new
    @attachment = Attachment.new
  end

  # GET /attachments/1/edit
  def edit
  end

  # POST /attachments
  # POST /attachments.json
  def create
    @attachment = Attachment.new(attachment_params)

    user_folder = Folder.find(User.find(session[:user_id]).home_folder_id)

    respond_to do |format|
      if @attachment.update(user_id: session[:user_id], folder_id: user_folder.id, file_type: 'User Uploaded Data')
        format.html { redirect_to attachments_path, notice: 'Attachment was successfully created.' }
        format.json { render action: 'show', status: :created, location: @attachment }
      else
        format.html { render action: 'new' }
        format.json { render json: @attachment.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /attachments/1
  # PATCH/PUT /attachments/1.json
  def update
    respond_to do |format|
      if @attachment.update(attachment_params)
        format.html { redirect_to @attachment, notice: 'Attachment was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @attachment.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /attachments/1
  # DELETE /attachments/1.json
  def destroy
    @attachment.destroy
    respond_to do |format|
      format.html { redirect_to attachments_url }
      format.json { head :no_content }
    end
  end

  #############################################################################
  def download
    send_data(@attachment.contents, filename: @attachment.file_name, type: @attachment.content_type)
  end

  private
  # Use callbacks to share common setup or constraints between actions.
  def set_attachment
    @attachment = Attachment.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def attachment_params
    params.require(:attachment).permit(:user_id, :folder_id, :file_name, :description, :file_type,
                                       :content_type, :updated_at, :contents_bytes, :contents, :is_parsed, :datafile)
  end


#############################################################################


end
