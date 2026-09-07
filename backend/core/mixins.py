class SchoolFilteredQuerysetMixin:

    def get_queryset(self):

        queryset = super().get_queryset()

        user = self.request.user

        if user.is_superuser:
            return queryset

        if (
            hasattr(user, "role")
            and user.role == "SUPER_ADMIN"
        ):
            return queryset

        return queryset.filter(
            school=user.school
        )