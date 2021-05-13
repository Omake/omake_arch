from views import Index, About, CategoryCreate, CourseList


route_list = {
    '/': Index(),
    '/about/': About(),
    '/create-category/': CategoryCreate(),
    '/courses-list/': CourseList()
}
