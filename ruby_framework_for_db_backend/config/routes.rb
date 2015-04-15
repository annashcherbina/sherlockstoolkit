Forensics::Application.routes.draw do
  resources :loci_groups

  resources :strs

  resources :snps

  resources :experimenters

  root "experiments#index"

  resources :loci

  resources :panel_loci

  resources :ethnicities

  resources :ancestries do
    collection do
      get :map
    end
  end


  resources :calls

  resources :primers

  resources :geographics

  resources :frequencies

  resources :locus_attributes

  resources :attachments do
    member do
      get :download
      post :upload
    end
  end

  resources :attachments

  resources :folders

  resources :panels

  resources :images do
    member do
      get :download
      get :show_img
      post :upload
    end # do
  end # images

  resources :points

  resources :kinships

  resources :relationships

  resources :allele_references

  resources :barcodes

  resources :comparisons

  resources :experiments do
    member do
      post 'form_action'
      get 'graph_best'
    end
  end

  resources :parameters

  resources :samples do
    collection do
      post 'form_action'
    end
  end

  resources :instruments

  resources :families

  resources :people

  resources :person_values

  resources :choices

  resources :attributes

  resources :logins do
    collection do
      get 'logout', 'logins'
      post 'verify'
    end # do
  end # do

  #match ':controller(/:action(/:id))', via: [:get, :post]

  # The priority is based upon order of creation: first created -> highest priority.
  # See how all your routes lay out with "rake routes".

  # You can have the root of your site routed with "root"
  # root 'welcome#index'

  # Example of regular route:
  #   get 'products/:id' => 'catalog#view'

  # Example of named route that can be invoked with purchase_url(id: product.id)
  #   get 'products/:id/purchase' => 'catalog#purchase', as: :purchase

  # Example resource route (maps HTTP verbs to controller actions automatically):
  #   resources :products

  # Example resource route with options:
  #   resources :products do
  #     member do
  #       get 'short'
  #       post 'toggle'
  #     end
  #
  #     collection do
  #       get 'sold'
  #     end
  #   end

  # Example resource route with sub-resources:
  #   resources :products do
  #     resources :comments, :sales
  #     resource :seller
  #   end

  # Example resource route with more complex sub-resources:
  #   resources :products do
  #     resources :comments
  #     resources :sales do
  #       get 'recent', on: :collection
  #     end
  #   end

  # Example resource route with concerns:
  #   concern :toggleable do
  #     post 'toggle'
  #   end
  #   resources :posts, concerns: :toggleable
  #   resources :photos, concerns: :toggleable

  # Example resource route within a namespace:
  #   namespace :admin do
  #     # Directs /admin/products/* to Admin::ProductsController
  #     # (app/controllers/admin/products_controller.rb)
  #     resources :products
  #   end
end
