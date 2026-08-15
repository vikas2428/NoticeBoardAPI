from functools import reduce


class AnalyticsService:
    """
    Provides analytics and advanced Python
    data processing for notices.
    """

    def get_statistics(self, notices):
        """
        Generate notice statistics using
        comprehensions, lambda, map, filter and reduce.
        """

        # List comprehension
        titles = [
            notice["title"]
            for notice in notices
        ]

        # Set comprehension
        categories = {
            notice["category"]
            for notice in notices
        }

        # filter() + lambda
        active_notices = list(
            filter(
                lambda notice: notice["status"] == "Active",
                notices
            )
        )

        archived_notices = list(
            filter(
                lambda notice: notice["status"] == "Archived",
                notices
            )
        )

        # map() + lambda
        title_lengths = list(
            map(
                lambda notice: len(notice["title"]),
                notices
            )
        )

        # reduce()
        total_title_characters = reduce(
            lambda total, length: total + length,
            title_lengths,
            0
        )

        # Dictionary comprehension
        category_counts = {
            category: len(
                [
                    notice
                    for notice in notices
                    if notice["category"] == category
                ]
            )
            for category in categories
        }

        return {
            "total_notices": len(notices),
            "active_notices": len(active_notices),
            "archived_notices": len(archived_notices),
            "categories": list(categories),
            "category_counts": category_counts,
            "titles": titles,
            "total_title_characters": total_title_characters
        }


analytics_service = AnalyticsService()