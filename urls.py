from views import Index, About, CategoryCreate, CourseList, CourseCreate


route_list = {
    '/': Index(),
    '/about/': About(),
    '/create-category/': CategoryCreate(),
    '/courses-list/': CourseList(),
    '/create-course/': CourseCreate(),
}
