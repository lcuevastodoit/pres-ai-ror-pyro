class ChatController < ApplicationController
  def ask
    @question = params[:question]
    @answer = ::ChatService.ask(@question)
    render partial: "chat/answer", locals: { question: @question, answer: @answer }
  rescue StandardError => e
    Rails.logger.error("Error in ChatController#ask: #{e.message}")
    render json: { error: "An error occurred while processing your request." },
      status: :internal_server_error
  end
end
