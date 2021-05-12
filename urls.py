from views import Index, About, CategoryCreate


route_list = {
    '/': Index(),
    '/about/': About(),
    '/create-category/': CategoryCreate(),
}
