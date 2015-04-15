class FoldersController < ApplicationController
  before_action :set_folder, only: [:show, :edit, :update, :destroy]

  # GET /folders
  # GET /folders.json
  def index
    @folders = Folder.where(level: 0)
  end

  # GET /folders/1
  # GET /folders/1.json
  def show
    @attachment_info = Attachment::grab_shortinfo(@folder.id)
    @image_info = Image::grab_shortinfo(@folder.id)
    @subfolders = Folder.where(parent_id: @folder.id).order('folders.name ASC')
    session[:last_viewed_folder_id] = @folder.id
  end

  # GET /folders/new
  def new
    @folder = Folder.new
  end

  # GET /folders/1/edit
  def edit
  end

  # POST /folders
  # POST /folders.json
  def create
    @folder = Folder.new(folder_params)
    #folder and its subfolders share the same user_id
    parent_folder = Folder.find(@folder.parent_id)
    @folder.user_id = parent_folder.user_id
    @folder.level = parent_folder.level + 1

    respond_to do |format|
      if @folder.save
        format.html { redirect_to @folder.parent, notice: 'Folder was successfully created.' }
        format.json { render action: 'show', status: :created, location: @folder }
      else
        format.html { render action: 'new' }
        format.json { render json: @folder.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /folders/1
  # PATCH/PUT /folders/1.json
  def update
    respond_to do |format|
      if @folder.update(folder_params)
        format.html { redirect_to @folder, notice: 'Folder was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @folder.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /folders/1
  # DELETE /folders/1.json
  def destroy
    @folder.destroy
    respond_to do |format|
      format.html { redirect_to folders_url }
      format.json { head :no_content }
    end
  end

  private
  # Use callbacks to share common setup or constraints between actions.
  def set_folder
    @folder = Folder.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def folder_params
    params.require(:folder).permit(:parent_id, :user_id, :name, :description, :level, :updated_at)
  end
end
