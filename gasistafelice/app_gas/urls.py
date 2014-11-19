
from django.conf.urls import patterns, include, url
import app_gas.views as gas_views

urlpatterns = patterns('',
    # Single action view
    url(r'^(?P<pk>\d+)/$', gas_views.GASDetailView.as_view(), 
        name='gas-detail'
    ),
    url(r'^create/$', gas_views.GASCreateView.as_view(), 
        name='gas-create'
    ),
    url(r'^(?P<pk>\d+)/edit/$', gas_views.GASUpdateView.as_view(),
        name='gas-update'
    ),
    #url(r'^(?P<pk>\d+)/vote/add/$', gas_views.ActionVoteView.as_view(), 
    #    name='action-vote-add'
    #),
    #url(r'^(?P<pk>\d+)/image/$', gas_views.ActionImageView.as_view(), 
    #    name='action-image'
    #),
    #url(r'^(?P<pk>\d+)/edit/politicians/$', gas_views.EditablePoliticianView.as_view(), 
    #    name='edit-politician'
    #),
    #url(r'^(?P<pk>\d+)/edit/(?P<attr>\w+)/$', gas_views.EditableParameterView.as_view(), 
    #    name='edit-parameter'
    #),

    ## Action related view (list of actions, comments for action, ...)
    #url(r'^comment/(?P<pk>\d+)/vote/add/$', gas_views.CommentVoteView.as_view(), 
    #    name='comment-vote-add'
    #),
    #url(r'^(?P<pk>\d+)/comment/add/$', gas_views.ActionCommentView.as_view(), 
    #    name='action-comment-add'
    #),
    #
    #url(r'^blogpost/(?P<pk>\d+)/comment/add/$', gas_views.BlogpostCommentView.as_view(), 
    #    name='blogpost-comment-add'
    #),
    #url(r'^(?P<pk>\d+)/blogpost/add/$', gas_views.ActionBlogpostView.as_view(), 
    #    name='action-blogpost-add'
    #),
    #url(r'^blogpost/(?P<pk>\d+)/edit/$', gas_views.UpdateActionBlogpostView.as_view(), 
    #    name='action-blogpost-edit'
    #),
    #url(r'^comment/(?P<pk>\d+)/vote/add/$', gas_views.CommentVoteView.as_view(), 
    #    name='comment-vote'
    #),
    ##follow/unfollow action
    #url(r'^(?P<pk>\d+)/follow/$', gas_views.ActionFollowView.as_view(), 
    #    name='action-follow'
    #),
    #url(r'^(?P<pk>\d+)/unfollow/$', gas_views.ActionUnfollowView.as_view(), 
    #    name='action-unfollow'
    #),
    ##request to a user to moderate action
    #url(r'^(?P<pk>\d+)/moderator/add/$', action_request_views.ActionModerationRequestView.as_view(), 
    #    name='action-moderation-request'
    #),
    ##private message between same Action referrers
    #url(r'^(?P<pk>\d+)/message/send/$', action_request_views.ActionMessageRequestView.as_view(), 
    #    name='action-message-send'
    #),
    ##remove moderator
    #url(r'^(?P<pk>\d+)/moderator/remove/$', gas_views.ActionModerationRemoveView.as_view(), 
    #    name='action-moderation-remove'
    #),
    ##request to change action status to the staff
    #url(r'^(?P<pk>\d+)/status/change/$', action_request_views.ActionSetStatusRequestView.as_view(), 
    #    name='action-status-change-request'
    #),

    #url(r'^filter/$', gas_views.FilteredActionListView.as_view(),
    #    name='actions-filter'
    #),

    ##categories navigation
    #url(r'^argument/(?P<pk>\d+)/$', gas_views.ActionByCategoryListView.as_view(),
    #    name='category-action-list'
    #),

    ##geonames navigation
    #url(r'^location/(?P<pk>\d+)/$', gas_views.ActionByGeonameListView.as_view(),
    #    name='geoname-action-list'
    #),

)

