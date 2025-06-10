require Rails.root.join('lib', 'ai_client')

class ChatService
  def self.ask(question)
    AiClient.ask(question)
  end
end
