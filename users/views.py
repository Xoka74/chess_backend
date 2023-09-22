from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.viewsets import ReadOnlyModelViewSet

from users import serializers
from users.forms import SignUpForm, UpdateUserForm
from django.contrib.auth import logout, login

from users.models import User, FriendRequest
from users.serializers import FriendRequestSerializer


@login_required(login_url='sign-in')
def profile(request):
    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UpdateUserForm(instance=request.user)

    return render(request, 'profile/profile.html', {
        'form': form
    })


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('client-history')
    form = SignUpForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('sign-in')

    return render(request, 'profile/sign_up.html', {'form': form})


def sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect('client-history')

    else:
        form = AuthenticationForm()
    return render(request, 'profile/login.html', {'form': form})


@login_required
def sign_out(request):
    logout(request)
    return redirect('sign-in')


class FriendRetrieveListViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserPreviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.friends.all()


class FriendRequestsViewSet(ReadOnlyModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = serializers.UserPreviewSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def sent(self, request):
        requests = self.request.user.sent_friend_requests.all()
        serializer = FriendRequestSerializer(requests, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def received(self, request, pk=None):
        requests = self.request.user.received_friend_requests.all()
        serializer = FriendRequestSerializer(requests, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def accept(self, request, pk=None):
        friend_request = self.get_object()
        user = self.request.user
        if friend_request.receiver == user:
            friend_request.accept()
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def decline(self, request):
        friend_request = self.get_object()
        user = self.request.user
        if friend_request.receiver == user:
            friend_request.decline()
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_404_NOT_FOUND)
