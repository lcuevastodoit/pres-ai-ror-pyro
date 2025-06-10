class QaPairController < ApplicationController
  def create
    @qa_pair = QaPair.create(question: params[:question], answer: params[:answer])
    render partial: "qa_pairs/new", locals: { qa: @qa_pair }
  end
end
