import os
import random
import time
import string
import platform
import json
import shutil
import errno
from django.conf import settings
from .forms import UploadFileForm
from .models import DeployPool, DeployStatus
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt


