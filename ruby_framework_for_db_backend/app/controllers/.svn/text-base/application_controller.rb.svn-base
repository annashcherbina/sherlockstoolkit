class ApplicationController < ActionController::Base
  # Prevent CSRF attacks by raising an exception.
  # For APIs, you may want to use :null_session instead.
  protect_from_forgery with: :exception

  before_filter :authenticate

  #############################################################################
  def authenticate
    redirect_to(logins_url) if session[:user_id].nil?
  end # authenticate

  def debug_msg(object)
    puts "####"
    puts "####"
    puts object
    puts "####"
    puts "####"
  end
end # class
