class ImagesController < ApplicationController
  before_action :set_image, only: [:show, :edit, :update, :destroy, :download, :show_img]

  # GET /images
  # GET /images.json
  def index
    if params[:folder_id]
      @folder = Folder.find(params[:folder_id])
      @images = @folder.images
    else
      @images = Image.all
    end
    @users_hash = Tools::to_hash(User.all)
    @folders_hash = Tools::to_hash(Folder.all)
  end

  # GET /images/1
  # GET /images/1.json
  def show
    @associated_image = @image.associated_image

    @experiments_details = []
    #if an image has been created by mixture/replicate/quality control module
    #then obtain the experiment details to details them
    if @image.description && @image.image_type != 'Read Counts'
      #breaks up the description by newline and maps the results to either
      #the header, such as "Truth:" or "Mixture:"
      #the a string defined by "$experiment.name - $experiment.hash_name"
      description_headers = @image.description.split("\n").map{ |line|
        tokens = line.split(' ')
        tokens.size > 1 ? "#{tokens[0]} - #{tokens[1].delete('()')}" : tokens[0]
      }


      @experiments_hash = Experiment.make_hash_by_name_and_hash_name
      @experiments_details = description_headers.map{ |line| @experiments_hash[line].present? ? @experiments_hash[line] : line }
      @experiments_details.uniq!
    end

    #sets up the owner, and group_name, and all parameters associated to the image or to its associated_image to @parameters
    @parameters = {}
    if @image.associated_attachment_id && !@image.associated_attachment.parameters.empty?
      @parameters['Parameter Owner'] = User.find(@image.associated_attachment.parameters.first.user_id).username
      @parameters['Group Name'] = @image.associated_attachment.parameters.first.group_name
      @image.associated_attachment.parameters.map{ |parameter| @parameters[parameter.name]=parameter.value }
    elsif @image.associated_image_id && @image.associated_image.associated_attachment_id && !@image.associated_image.associated_attachment.parameters.empty?
      @parameters['Parameter Owner'] = User.find(@image.associated_image.associated_attachment.parameters.first.user_id).username
      @parameters['Group Name'] = @image.associated_image.associated_attachment.parameters.first.group_name
      @image.associated_image.associated_attachment.parameters.map{ |parameter| @parameters[parameter.name]=parameter.value }
    end

  end

  # GET /images/new
  def new
    @image = Image.new
  end

  # GET /images/1/edit
  def edit
  end

  # POST /images
  # POST /images.json
  def create
    @image = Image.new(image_params)
    @image.user_id = session[:user_id]
    @image.folder_id = Folder.where(user_id: session[:user_id], level: 1).first.id

    respond_to do |format|
      if @image.save
        format.html { redirect_to @image, notice: 'Image was successfully uploaded.' }
        format.json { render action: 'show', status: :created, location: @image }
      else
        format.html { render action: 'new' }
        format.json { render json: @image.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /images/1
  # PATCH/PUT /images/1.json
  def update
    respond_to do |format|
      if @image.update(image_params)
        format.html { redirect_to @image, notice: 'Image was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @image.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /images/1
  # DELETE /images/1.json
  def destroy
    @image.destroy
    respond_to do |format|
      format.html { redirect_to images_url }
      format.json { head :no_content }
    end
  end

  def download
    send_data(@image.picture, filename: @image.file_name, type: @image.content_type)
  end

  def show_img
    send_data(@image.picture, filename: @image.file_name, :type => @image.content_type, :disposition => 'inline')
  end

  private
  #   Use callbacks to share common setup or constraints between actions.
  def set_image
    @image = Image.find(params[:id])
  end

  #Never trust parameters from the scary internet, only allow the white list through.
  def image_params
    params.require(:image).permit(:folder_id, :file_name, :description, :image_type, :content_type, :picture_bytes, :created_at, :picture, :datafile)
  end
end
