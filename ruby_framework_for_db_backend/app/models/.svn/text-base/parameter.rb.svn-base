class Parameter < ActiveRecord::Base
  has_and_belongs_to_many :attachments

  validates :group_name, :category, :name, :value, { presence: true }

  private

  INTEGER_PARAMS = [
      'Minimum Reads per Locus (integer)',
      'Maximum mismatches to plot for PD (integer)',
      'Maximum impossible for Kinship (integer)',
      'Minimum number of Kidd SNPs present (integer 1 to 128)',
      'Minimum ancestry contributions to report (integer)',
      'Genetic algorithm runs for subject (number to be averaged)'
  ]

  PERCENTAGE_PARAMS = [
      'Reference - MAF for 2 Minor Alleles (lower bound %)',
      'Reference - MAF for 1 Minor Allele (lower bound %)',
      'Reference - MAF for 1 Minor Allele (upper bound %)',
      'Reference - MAF for 0 Minor Alleles (upper bound %)',
      'Mixture - MAF for 2 Minor Alleles (lower bound %)',
      'Mixture - MAF for 1 Minor Allele (lower bound %)',
      'Mixture - MAF for 1 Minor Allele (upper bound %)',
      'Mixture - MAF for 0 Minor Alleles (upper bound %)',
      'Strand Bias Ratio (upper bound %)',
      'Ambiguous Bias Ratio (upper bound %)',
      'Low Calls Ratio (upper bound %)',
      'Minimum ancestry contributions to report (%)'
  ]

  #given an array of category names
  #gets all the system default parameters
  def self.get_default_params(category_array)
    default_params_hash = {}

    system_user_id = User.find_by_name('System').id
    default_params = Parameter.where(user_id: system_user_id, group_name: 'System Defaults', category: category_array)
    default_params.each do |param|
      if default_params_hash[param.category].present?
        default_params_hash[param.category] << param
      else
        default_params_hash[param.category] = [param]
      end
    end

    default_params_hash
  end


  #returns a multilayered hash of all the latest parameters in the style of
  #parameters[$OWNER_USERNAME][$PARAMETER_GROUP_NAME][$PARAMETER_NAME] = $PARAMETER_VALUE
  def self.get_all_latest
    parameters = {}

    params_hash = Tools::to_hash(Parameter.all).sort
    params_hash.each do |param_id, parameter|
      parameters[parameter.user_id] ||= {}
      parameters[parameter.user_id][parameter.group_name] ||= {}
      parameters[parameter.user_id][parameter.group_name][parameter.name] = parameter.value
    end

    parameters
  end

  def self.validate_parameter(name, value)
    #making sure the value may be cast as a float
    begin
      value = Float(value)
    rescue
      return false
    end

    #checking the ratio params
    return false if PERCENTAGE_PARAMS.include?(name) && (value < 0 || value > 100)

    #checking the integer params
    return false if INTEGER_PARAMS.include?(name) && (value < 0  || value%1 != 0)

    #the following validation rules are to see if the value is higher than the max determined by the parameter name
    return false if name=='Minimum number of Kidd SNPs present (out of 128)' && value >= 128
    return false if name=='Maximum mismatches to plot for PD' && value > 200
    return false if name=='Minimum ancestry contributions to report (number)' && value > Ethnicity.count - 1 #the -1 is to account for global
    return true
  end

  def self.get_system_default_parameters
    system_user = User.find_by(username: 'SYSTEM')
    param_order = ['Allele Calling', 'Bad SNPs', 'Mixture', 'Kinship', 'Ancestry']
    #gets the system parameters in order, even if new system default params are added in later
    Parameter.where(user_id: system_user.id, group_name: 'System Defaults').sort_by { |p| param_order.index(p.category)}
  end


  def self.update_and_create_groups(user_id, username, params)
    response = ''
    valid_parameter_found = false
    system_params = Parameter.get_system_default_parameters

    if params[:new_group_name].empty?
      if params[:param_owner] == user_id
        group_name = params[:param_group]
      else
        group_name = "#{username}-#{params[:param_group]}"
      end
    else
      group_name = params[:new_group_name]
    end

    parameters = []
    invalid_hash = {}
    params_hash = {}
    params_hash[:group_name] = group_name
    params_hash[:user_id] = user_id

    new = params[:new_exp_params].delete_if{ |k,v| v.empty? }
    old = params[:old_exp_params]

    system_params.each do |system_param|
      params_hash[:name] = system_param.name
      params_hash[:category] = system_param.category
      #if the new value exists for that system param name:
      if new.keys.include?(system_param.name)
        #if the entered values passes the validations
        if Parameter.validate_parameter(system_param.name, new[system_param.name])
          params_hash[:value] = new[system_param.name]
          valid_parameter_found = true
        else
          params_hash[:value] = system.param.value
          invalid_hash[system_param.name] = new[system_param.name]
        end
      #use old params
      elsif old.keys.include?(system_param.name)
        params_hash[:value] = old[system_param.name]
      #use system params
      else
        params_hash[:value] = system_param.value
      end
      parameters << Parameter.new(params_hash)
    end

    #output response message indicating what has been done
    if valid_parameter_found
      Parameter.import(parameters)
      response += "<p>Created/Updated Parameter Group: #{group_name} for #{username}.</p>"
    else
      response += '<p>Nothing done.</p>'
    end

    #lists out invalid values for the user
    unless invalid_hash.empty?
      response += 'Invalid values detected:<ul>'
      invalid_hash.each do |name, value|
        response += "<li>Parameter #{name}: #{value}</li>"
      end
      response += '</li></ul>'
    end

    response
  end


end
