module FoldersHelper
  def is_empty(folder)
    if folder.children.empty? && folder.images.empty? && folder.attachments.empty?
      true
    else
      false
    end
  end
end
