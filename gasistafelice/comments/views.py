 
# Copyright (C) 2008 Laboratori Guglielmo Marconi S.p.A. <http://www.labs.it>
#
# This file is part of SANET
# SANET is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License
#
# SANET is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with SANET. If not, see <http://www.gnu.org/licenses/>.

from django.contrib.comments.views.moderation import *
from django.contrib.comments.models import Comment

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

# Modified from django.contrib.comments.views.moderation
# WARNING !!!! All commments are deleted by "fake_moderator" user

#---------------------------------------------------------------------#
#                                                                     #
#---------------------------------------------------------------------#

#@login_required #to manage permission to delet notes
def delete(request, comment_id, next=None):
    """
    Deletes a comment. Confirmation on GET, action on POST. Requires the "can
    moderate comments" permission.

    Templates: `comments/delete.html`,
    Context:
        comment
            the flagged `comments.comment` object
    """
    comment = get_object_or_404(comments.get_model(), pk=comment_id, site__pk=settings.SITE_ID)

    # Delete on POST
    if request.method == 'POST':
        moderator, created = User.objects.get_or_create(username="fake_moderator")

        # Flag the comment as deleted instead of actually deleting it.
        flag, created = comments.models.CommentFlag.objects.get_or_create(
            comment = comment,
            user    = moderator,
            flag    = comments.models.CommentFlag.MODERATOR_DELETION
        )
        comment.is_removed = True
        comment.save()
        signals.comment_was_flagged.send(
            sender  = comment.__class__,
            comment = comment,
            flag    = flag,
            created = created,
            request = request,
        )
        return next_redirect(request.POST.copy(), next, delete_done, c=comment.pk)

    # Render a form on GET
    else:
        return render_to_response('comments/delete.html',
            {'comment': comment, "next": next},
            template.RequestContext(request)
        )

#---------------------------------------------------------------------#
#                                                                     #
#---------------------------------------------------------------------#


class NoteList(list):

	def __init__(self, items, count):
		self.count = count
		super(NoteList, self).__init__(items)


def get_all_notes( ignore_resources = None):

	all_comments = Comment.objects.filter(is_removed=False).select_related() 
	notes_d = { }
	for comment in all_comments:
		obj = comment.content_object
		
		if obj != None:
			if ignore_resources:
				if obj.__class__.__name__.lower() in ignore_resources:
					continue
		
		#print "NOTES: " , obj, type(obj)
		notes_d[obj] = notes_d.get(obj, []) + [comment]

	notes = NoteList(notes_d.items(), all_comments.count())
	notes.sort(cmp=lambda x,y: cmp(x[0],y[0]))
	
	return notes


def get_notes_for( resources ):
	all_comments = Comment.objects.filter(is_removed=False).select_related().all()
	notes_d = { }
	for comment in all_comments:
		obj = comment.content_object
		if obj != None:
			if obj in resources:
                                notes_d[obj] = notes_d.get(obj, []) + [comment]

	notes = NoteList(notes_d.items(), all_comments.count())
	notes.sort(cmp=lambda x,y: cmp(x[0],y[0]))

	return notes

#---------------------------------------------------------------------#
#                                                                     #
#---------------------------------------------------------------------#

#@login_required #to filter notes according to user
#def show_all(request):
#context = { 'notes' : get_all_notes() }
#	return render_to_response('comments/show_all.html', context)

