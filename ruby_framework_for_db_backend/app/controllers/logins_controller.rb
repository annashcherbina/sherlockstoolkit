############################################################################
class LoginsController < ApplicationController

  skip_before_filter :authenticate

#############################################################################
  def clear_sessions
    session[:user_id] = nil
    session[:username] = nil
    session[:is_admin] = false
    session[:last_viewed_folder_id] = nil
    session[:home_folder_id] = nil
  end  # clear_sessions

#############################################################################
  # GET /users
  # GET /users.xml
  def index
    clear_sessions
  end  # index

#############################################################################
  def show
    redirect_to(logins_url)
  end

# show

#  ############################################################################
  def logout
    clear_sessions
    redirect_to(logins_url)
  end

# logout

#############################################################################
  def verify
        username = params[:username]
    @user = User.find_by_username(username)
    if @user.nil?
      logger.debug "#{username} -- user not found!!!"
    else
      logger.debug "#{username} -- user found!"
    end
    if  @user != nil
      # Verify the password
      if @user.hashed_password.blank?
        @user.password = params[:password]
        @user.save
      else
        # Validate the given password
        if !@user.verify_password(params[:password])
          flash[:notice] = "Invalid userid/password combination"
          redirect_to(logins_url)
          return
        end #  if
      end #  if

      session[:user_id] = @user.id
      session[:username] = username
      session[:is_admin] = @user.is_admin
      session[:home_folder_id] = @user.home_folder_id

      flash[:notice] = "Welcome #{@user.name}"

          redirect_to(experiments_url)
      return
    else
      flash[:notice] = "Unknown userid/password combination."
    end #  if

        #not found
    flash[:notice] = "Login name '#{username}' was not found."
    redirect_to(logins_url)
  end

# verify

#  ############################################################################
  def reset_password
    @user = User.find(params[:id])
    if @user.hashed_password.blank?
      flash[:notice] = "User's password is blank"
      redirect_to(users_path)
    else
      @user.hashed_password = ""
      @user.save
      flash[:notice] = "Password was successfuly reset"
      redirect_to(users_path)
    end # If
  end # reset_password

#############################################################################
end #  class LoginsController