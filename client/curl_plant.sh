curl -X POST \
	-H "Content-Type: application/json" \
	-d @p1.json \
	http://localhost:8000/api/plants
curl -X POST \
	-H "Content-Type: application/json" \
	-d @p2.json \
	http://localhost:8000/api/plants
