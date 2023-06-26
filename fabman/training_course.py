"""Defines and handles the TrainingCourse object"""
import requests
from fabman.fabman_object import FabmanObject

class TrainingCourse(FabmanObject):
    """TrainingCourse Object handles all API calls that operate on a single TrainingCourse.
    """
    
    def __str__(self):
        return f"TrainingCourse #{self.id}: {self.name}"
    
    def update_course(self, **kwargs) -> requests.Response:
        """
        Update the training course with the given data. Will create the data
        if the training course does not exist.
        
        Calls "PUT /training-courses/{id}"
        Documentation https://fabman.io/api/v1/documentation#/training-courses/putTrainingcoursesId
        """
        uri = f"/training-courses/{self.id}"
        
        response = self._requester.request(
            "PUT", uri, _kwargs=kwargs
        )
        
        return response.json()
    
    def delete_course(self, **kwargs) -> requests.Response:
        """
        Delete the training course. *WARNING: THIS CANNOT BE UNDONE.*
        
        Calls "DELETE /training-courses/{id}"
        Documentation https://fabman.io/api/v1/documentation#/training-courses/deleteTrainingcoursesId
        """
        uri = f"/training-courses/{self.id}"
        
        response = self._requester.request(
            "DELETE", uri, _kwargs=kwargs
        )
        
        return response.json()