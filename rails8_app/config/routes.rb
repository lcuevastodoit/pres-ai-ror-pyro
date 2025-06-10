Rails.application.routes.draw do
  root "home#index"
  resources :qa_pairs
  get "chat/ask", to: "chat#ask"
end
