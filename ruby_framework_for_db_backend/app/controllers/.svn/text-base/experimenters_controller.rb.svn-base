class ExperimentersController < ApplicationController
  before_action :set_experimenter, only: [:show, :edit, :update, :destroy]

  # GET /experimenters
  # GET /experimenters.json
  def index
    @experimenters = Experimenter.all
  end

  # GET /experimenters/1
  # GET /experimenters/1.json
  def show
  end

  # GET /experimenters/new
  def new
    @experimenter = Experimenter.new
  end

  # GET /experimenters/1/edit
  def edit
  end

  # POST /experimenters
  # POST /experimenters.json
  def create
    @experimenter = Experimenter.new(experimenter_params)

    respond_to do |format|
      if @experimenter.save
        format.html { redirect_to @experimenter, notice: 'Experimenter was successfully created.' }
        format.json { render action: 'show', status: :created, location: @experimenter }
      else
        format.html { render action: 'new' }
        format.json { render json: @experimenter.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /experimenters/1
  # PATCH/PUT /experimenters/1.json
  def update
    respond_to do |format|
      if @experimenter.update(experimenter_params)
        format.html { redirect_to @experimenter, notice: 'Experimenter was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @experimenter.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /experimenters/1
  # DELETE /experimenters/1.json
  def destroy
    @experimenter.destroy
    respond_to do |format|
      format.html { redirect_to experimenters_url }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_experimenter
      @experimenter = Experimenter.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def experimenter_params
      params.require(:experimenter).permit(:experiment_id, :person_id, :role, :empcr, :uncertain_empcr, :seq, :uncertain_seq)
    end
end
