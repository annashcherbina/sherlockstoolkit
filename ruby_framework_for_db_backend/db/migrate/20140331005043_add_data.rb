class AddData < ActiveRecord::Migration
  def change
      Instrument.create(name: 'PGM' )
      Instrument.create(name: 'Proton' )
      Instrument.create(name: '454')
      Instrument.create(name: 'Illumina')
      Instrument.create(name: 'PacBio')

      system_user = User.create(username: 'SYSTEM', name: 'SYSTEM', is_admin: true)
      results_folder = Folder.create(user_id: system_user.id, name: 'Results', description: 'Results', level: 0)
      Folder.create(user_id: system_user.id, parent_id: results_folder.id, name: 'Mixture', description: 'Mixture Module', level: 1)
      Folder.create(user_id: system_user.id, parent_id: results_folder.id, name: 'Replicate', description: 'Replicate Module', level: 1)
      Folder.create(user_id: system_user.id, parent_id: results_folder.id, name: 'Kinship', description: 'Kinship Module', level: 1)
      Folder.create(user_id: system_user.id, parent_id: results_folder.id, name: 'Ancestry', description: 'Ancestry Module', level: 1)
      Folder.create(user_id: system_user.id, parent_id: results_folder.id, name: 'Quality Control', description: 'Quality Control Module', level: 1)

      Folder.create(user_id: system_user.id, name: 'Panel Data', description: 'Panel Data Files', level: 0)
      Folder.create(user_id: system_user.id, name: 'Users', description: 'User Specific Data', level: 0)

      User.create_with_folder(username: 'da23452', name: 'Darrell O. Ricke', email: 'Darrell.Ricke@ll.mit.edu', is_admin: true)
      User.create_with_folder(username: 'an23471', name: 'Anna Shcherbina', email: 'Anna.Shcherbina@ll.mit.edu', is_admin: true)
      User.create_with_folder(username: 'ne24918', name: 'Nelson Chiu', email: 'Nelson.Chiu@ll.mit.edu', is_admin: true)
      User.create_with_folder(username: 'demo', name: 'demo user', email: '', is_admin: false)
      User.create_with_folder(username: 'er17595', name: 'Eric Schwoebel', email: 'Eric.Schwoebel@ll.mit.edu', is_admin: false)
      User.create_with_folder(username: 'ma16625', name: 'Martha Petrovick', email: 'petrovick@ll.mit.edu', is_admin: false)
      User.create_with_folder(username: 'ta17849', name: 'Tara Boettcher', email: 'dactyl@ll.mit.edu', is_admin: false)
      User.create_with_folder(username: 'ch17759', name: 'Christina Zook', email: 'petrovick@ll.mit.edu', is_admin: false)
      User.create_with_folder(username: 'jo17045', name: 'Johanna Bobrow', email: 'johanna@ll.mit.edu', is_admin: false)
      User.create_with_folder(username: 'ja17162', name: 'James Harper', email: 'harper@ll.mit.edu', is_admin: false)
      User.create_with_folder(username: 'ed15447', name: 'Ed Wack', email: 'wack@ll.mit.edu', is_admin: false)

      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Allele Calling', name: 'Minimum Reads per Locus (integer)', value: 50)
      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Allele Calling', name: 'Reference - MAF for 2 Minor Alleles (lower bound %)', value: 90)
      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Allele Calling', name: 'Reference - MAF for 1 Minor Allele (lower bound %)', value: 30)
      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Allele Calling', name: 'Reference - MAF for 1 Minor Allele (upper bound %)', value: 70)
      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Allele Calling', name: 'Reference - MAF for 0 Minor Alleles (upper bound %)', value: 10)

      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Allele Calling', name: 'Mixture - MAF for 2 Minor Alleles (lower bound %)', value: 99)
      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Allele Calling', name: 'Mixture - MAF for 1 Minor Allele (lower bound %)', value: 40)
      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Allele Calling', name: 'Mixture - MAF for 1 Minor Allele (upper bound %)', value: 60)
      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Allele Calling', name: 'Mixture - MAF for 0 Minor Alleles (upper bound %)', value: 1)

      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Bad SNPs', name: 'Strand Bias Ratio (upper bound %)', value: 90)
      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Bad SNPs', name: 'Ambiguous Bias Ratio (upper bound %)', value: 90)
      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Bad SNPs', name: 'Low Calls Ratio (upper bound %)', value: 90)

      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Mixture', name: 'Maximum mismatches to plot for PD (integer)', value: 100)

      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Kinship', name: 'Maximum impossible for Kinship (integer)', value: 60)

      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Ancestry', name: 'Minimum number of Kidd SNPs present (integer 1 to 128)', value: 30)
      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Ancestry', name: 'Minimum ancestry contributions to report (integer)', value: 4)
      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Ancestry', name: 'Minimum ancestry contributions to report (%)', value: 10)
      Parameter.create(user_id: system_user.id, group_name: 'System Defaults', category: 'Ancestry', name: 'Genetic algorithm runs for subject (number to be averaged)', value: 2)

  end  # change
end  # class
