class ChatController < ApplicationController
  def ask
    @answer = ::ChatService.ask(params[:question])
    render partial: "chat/answer", locals: { answer: @answer }
  rescue StandardError => e
    Rails.logger.error("Error in ChatController#ask: #{e.message}")
    render json: { error: "An error occurred while processing your request." },
      status: :internal_server_error
  end
end
