Rails.application.routes.draw do
  root "home#index"
  resources :qa_pairs, only: [:index, :create, :destroy]
  post "chat/ask", to: "chat#ask"
end
