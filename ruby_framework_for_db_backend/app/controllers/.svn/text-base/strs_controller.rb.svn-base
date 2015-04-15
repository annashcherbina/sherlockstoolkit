class STRsController < ApplicationController
  before_action :set_str, only: [:show, :edit, :update, :destroy]

  # GET /strs
  # GET /strs.json
  def index
    @strs = STR.all
  end

  # GET /strs/1
  # GET /strs/1.json
  def show
  end

  # GET /strs/new
  def new
    @str = STR.new
  end

  # GET /strs/1/edit
  def edit
  end

  # POST /strs
  # POST /strs.json
  def create
    @str = STR.new(str_params)

    respond_to do |format|
      if @str.save
        format.html { redirect_to @str, notice: 'STR was successfully created.' }
        format.json { render action: 'show', status: :created, location: @str }
      else
        format.html { render action: 'new' }
        format.json { render json: @str.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /strs/1
  # PATCH/PUT /strs/1.json
  def update
    respond_to do |format|
      if @str.update(str_params)
        format.html { redirect_to @str, notice: 'STR was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @str.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /strs/1
  # DELETE /strs/1.json
  def destroy
    @str.destroy
    respond_to do |format|
      format.html { redirect_to strs_url }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_str
      @str = STR.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def str_params
      params.require(:str).permit(:experiment_id, :primer_id, :locus_id, :sample_id, :name, :is_stutter, :is_novel_allele, :is_novel_flank, :novel_flank_name, :flank5, :flank3, :str_call)
    end
end
