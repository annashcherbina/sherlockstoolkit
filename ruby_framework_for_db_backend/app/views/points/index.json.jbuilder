json.array!(@points) do |point|
  json.extract! point, :id, :points_id, :image_id, :type_of_point, :qual
  json.url point_url(point, format: :json)
end
