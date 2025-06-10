class CreateQaPairs < ActiveRecord::Migration[8.0]
  def change
    create_table :qa_pairs do |t|
      t.string :question
      t.string :answer

      t.timestamps
    end
  end
end
