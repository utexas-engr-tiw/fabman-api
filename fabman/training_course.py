"""Defines and handles the TrainingCourse object"""
import requests

from fabman.fabman_object import FabmanObject


class TrainingCourse(FabmanObject):
    """TrainingCourse Object handles all API calls that operate on a single TrainingCourse."""

    def __str__(self):
        return f"TrainingCourse #{self.id}: {self.title}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Delete the training course. *WARNING: THIS CANNOT BE UNDONE.*

        :calls: "DELETE /training-courses/{id}" \
		<https://fabman.io/api/v1/documentation#/training-courses/deleteTrainingcoursesId>
  
        :return: response information of call
        :rtype: requests.Response
        """
        uri = f"/training-courses/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def update(self, **kwargs) -> None:
        """
        Update the training course with the given data. Will create the data
        if the training course does not exist.

        :calls: "PUT /training-courses/{id}" \
		<https://fabman.io/api/v1/documentation#/training-courses/putTrainingcoursesId>
  
        :return: None -- attributes are updated in place
        :rtype: None
        """
        uri = f"/training-courses/{self.id}"

        kwargs.update({"lockVersion": self.lockVersion})
        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)
