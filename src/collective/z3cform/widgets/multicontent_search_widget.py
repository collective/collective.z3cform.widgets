# -*- coding: utf-8 -*-

from zope.component import getMultiAdapter
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer
from zope.i18n import translate

from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.vocabularies.catalog import parse_query
from plone.formwidget.contenttree.widget import MultiContentTreeWidget, Fetch
from plone.formwidget.autocomplete.widget import AutocompleteSearch

from Products.CMFCore.utils import getToolByName

import z3c.form.interfaces
import z3c.form.widget

LIMIT = 10


class RelatedSearch(AutocompleteSearch):

    display_template = ViewPageTemplateFile('related_search.pt')

    def __call__(self):
        # We want to check that the user was indeed allowed to access the
        # form for this widget. We can only this now, since security isn't
        # applied yet during traversal.
        self.validate_access()
        limit = LIMIT
        query = self.request.get('q', None)
        offset = int(self.request.get('offset', 0))
        self.show_more = True
        if not query:
            query = ''
        # Update the widget before accessing the source.
        # The source was only bound without security applied
        # during traversal before.
        self.context.update()
        source = self.context.bound_source  # XXX: this is not used
        # TODO: use limit?
        result = self.search(query, limit=limit, offset=offset)
        portal_state = getMultiAdapter((self.context, self.request),
                                          name=u'plone_portal_state')
        portal = portal_state.portal()

        strategy = getMultiAdapter((portal, self.context), INavtreeStrategy)

        data = [strategy.decoratorFactory({'item':node}) for node in result]
        if len(data) < LIMIT:
            self.show_more = False
        result = self.filterSelected(data)
        return self.display_template(children=result, level=1, offset=offset + limit)

    def getTermByBrain(self, brain):
        # Ask the widget
        return self.context.getTermByBrain(brain)

    def filterSelected(self, data):
        result = self.context.filterSelected({'children': data})
        return result.get('children', [])

    def search(self, query='', limit=None, offset=0):
        portal_tool = getToolByName(self.context, "portal_url")
        self.portal_path = portal_tool.getPortalPath()
        source = self.context.bound_source
        catalog_query = source.selectable_filter.criteria.copy()
        catalog_query.update(parse_query(query, self.portal_path))
        catalog_query['sort_on'] = 'created'
        catalog_query['sort_order'] = 'descending'

        if limit and 'sort_limit' not in catalog_query and offset == 0:
            catalog_query['sort_limit'] = limit
        elif limit and 'sort_limit' not in catalog_query:
            catalog_query['sort_limit'] = offset + limit

        results = source.catalog(**catalog_query)
        if offset != 0:
            results = results[offset:(offset + limit)]
        return results


class FetchRelated(Fetch):
    fragment_template = ViewPageTemplateFile('fragment.pt')
    recurse_template = ViewPageTemplateFile('input_recurse.pt')


class MultiContentSearchWidget(MultiContentTreeWidget):
    display_template = ViewPageTemplateFile('related_display.pt')
    input_template = ViewPageTemplateFile('related_input.pt')
    recurse_template = ViewPageTemplateFile('related_recurse.pt')
    checkbox_template = ViewPageTemplateFile('improved_checkbox_input.pt')
    selected_template = ViewPageTemplateFile('related_search.pt')

    def update(self):
        super(MultiContentSearchWidget, self).update()

        batch = 10
        prev = self.request.get("batch.prev", None)
        next = self.request.get("batch.next", None)
        self.checked = []
        self.unchecked = []
        self.show_prev = False
        self.show_next = False

        try:
            self.related_batch = int(self.request.get("related_batch", 1))
        except:
            self.related_batch = 1

        if prev:
            self.related_batch -= 1
        elif next:
            self.related_batch += 1

        for i in self.items:
            if i['checked']:
                self.checked.append(i)
            else:
                self.unchecked.append(i)

        lower = (self.related_batch - 1) * batch
        upper = self.related_batch * batch

        if len(self.unchecked) >= upper:
            self.show_next = True

        if self.related_batch != 1:
            self.show_prev = True

        self.unchecked.sort(key=lambda x: x['id'])
        self.unchecked = self.unchecked[lower:upper]

        self.items = self.checked + self.unchecked

    def render_tree(self, relPath=None, query=None, limit=LIMIT, offset=0):
        self.show_more = True
        content = self.context    # XXX: this is not used
        portal_state = getMultiAdapter((self.context, self.request),
                                          name=u'plone_portal_state')
        portal = portal_state.portal()
        source = self.bound_source

        if query is not None:
            source.navigation_tree_query = query
        strategy = getMultiAdapter((portal, self), INavtreeStrategy)
        if relPath is not None:
            root_path = portal_state.navigation_root_path()
            rel_path = root_path + '/' + relPath
            strategy.rootPath = rel_path
        if not source.selectable_filter.criteria:
            data = buildFolderTree(portal,
                               obj=portal,
                               query=source.navigation_tree_query,
                               strategy=strategy)
        else:
            result = self.getRelated(limit=10)
            if len(result) < LIMIT:
                self.show_more = False
            data = self.brainsToTerms(result)
        result = self.filterSelected(data)
        return self.recurse_template(
                                    children=result.get('children', []),
                                    level=1,
                                    offset=offset + limit)

    def getRelated(self, query='', limit=None):
        portal_tool = getToolByName(self.context, "portal_url")
        portal_path = portal_tool.getPortalPath()
        source = self.bound_source
        catalog_query = source.selectable_filter.criteria.copy()
        catalog_query.update(parse_query(query, portal_path))
        catalog_query['sort_on'] = 'created'
        catalog_query['sort_order'] = 'descending'
        if limit and 'sort_limit' not in catalog_query:
            catalog_query['sort_limit'] = limit
        results = source.catalog(**catalog_query)
        return results

    def filterSelected(self, data):
        result = []
        selected_ids = [i['id'] for i in self.get_selected()] + [self.context.getId()]
        for item in data.get('children', []):
            if 'id' in item.keys() and item['id'] not in selected_ids:
                result.append(item)
        return {'children': result}

    def brainsToTerms(self, brains):
        portal_state = getMultiAdapter((self.context, self.request),
                                          name=u'plone_portal_state')
        portal = portal_state.portal()

        strategy = getMultiAdapter((portal, self), INavtreeStrategy)
        result = []
        for node in brains:
            term = strategy.decoratorFactory({'item': node})
            term['children'] = []
            result.append(term)
        return {'children': result}

    def get_selected(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                         name=u'plone_portal_state')
        portal = portal_state.portal()
        strategy = getMultiAdapter((portal, self), INavtreeStrategy)

        catalog = getToolByName(self.context, 'portal_catalog')
        items = []
        for related in self.items:
            folder_path = related['value']
            result = catalog(path={'query': folder_path, 'depth': 0})
            if result:
                brain = result[0]
                items.append(strategy.decoratorFactory({'item': brain}))
        return items

    def render_selected(self):
        items = self.get_selected()
        return self.selected_template(children=items, level=1)

    def renderQueryWidget(self):
        return self.checkbox_template()

    def related_url(self):
        """Generate the URL that returns autocomplete results for this form
        """
        form_url = self.request.getURL()

        return "%s/++widget++%s/@@related-search" % (
            form_url, self.name)

    # XXX: why do we have this bunch of JS code here and not in a template?
    def js_extra(self):
        form_url = self.request.getURL()
        url = "%s/++widget++%s/@@contenttree-related-fetch" % (form_url, self.name)

        return """\
                $('#%(id)s-widgets-query').each(function() {
                    if($(this).siblings('input.searchButton').length > 0) { return; }
                    $(document.createElement('input'))
                        .attr({
                            'type': 'button',
                            'value': '%(button_val)s'
                        })
                        .addClass('searchButton')
                        .click( function () {
                            var parent = $(this).parents("*[id$='-autocomplete']")
                            var window = parent.siblings("*[id$='-contenttree-window']")
                            window.showDialog();
                            infiniteScrollItems();
                        }).insertAfter($(this));
                });
                $('#%(id)s-contenttree-window').find('.contentTreeAdd').unbind('click').click(function () {
                    $(this).contentTreeAddRelated();
                });
                $('#%(id)s-contenttree-window').find('.contentTreeCancel').unbind('click').click(function () {
                    $(this).contentTreeCancel();
                });
                $('#%(id)s-widgets-query').after(" ");
                $('#%(id)s-contenttree').contentTree(
                    {
                        script: '%(url)s',
                        folderEvent: '%(folderEvent)s',
                        selectEvent: '%(selectEvent)s',
                        expandSpeed: %(expandSpeed)d,
                        collapseSpeed: %(collapseSpeed)s,
                        multiFolder: %(multiFolder)s,
                        multiSelect: %(multiSelect)s,
                    },
                    function(event, selected, data, title) {
                        // alert(event + ', ' + selected + ', ' + data + ', ' + title);
                    }
                );

                function infiniteScrollItems() {
                    var opts = {context:'#%(id)s-contenttree', offset: '%(perc)s'};
                    var $footer = $("#%(id)s-contenttree #show-more-items-results");
                    if ($footer.length) {
                        $footer.waypoint(function(event, direction) {
                            $footer.waypoint('remove');
                            if(direction == 'down') {
                                $("#show-more-items-results a").trigger("click");
                            }
                        }, opts);
                    }

                }

                function appendMoreItems(offset) {
                    $("#show-more-items-results").remove();
                    var query = document.getElementById('relatedWidget-search-input').value;

                    jQuery.ajax({type: 'POST',
                                url: '%(urlSearch)s',
                                async : true,
                                data: {'q':query,
                                        'offset':offset},
                                success: function(results) {
                                        $("ul#%(id)s-contenttree").append(results);
                                        hideMoreSpinner();
                                        infiniteScrollItems();
                                        }
                                    });
                }

                function relatedWidgetSearchFilter(url) {

                  $("#form-widgets-relatedItems-contenttree").attr("data-page", "0");
                  var queryVal = $("#relatedWidget-search-input").val();
                  $.ajax({
                    url: url,
                    data: {'q':queryVal},
                    success: function(info){
                      $(".relatedWidget ul.from").html(info);
                      hideSearchSpinner();
                      return false;
                    }
                  });
                  return false;
                }

                $("#show-more-items-results a").unbind("click");
                $("#show-more-items-results a").live("click", function(event) {
                    event.preventDefault();
                    var offset = $("#show-more-items-results").attr("data-offset");
                    showMoreSpinner();
                    appendMoreItems(offset);
                    return false;
                });
                $("#relatedWidget-search-button").unbind("click")
                $("#relatedWidget-search-button").live("click", function(event) {
                    event.preventDefault();
                    var urlSearch = '%(urlSearch)s'
                    showSearchSpinner();
                    relatedWidgetSearchFilter(urlSearch);
                    return false;
                });

                function showSearchSpinner() {
                $("#related-search-spinner").css("display", "inline");
                }

                function hideSearchSpinner() {
                $("#related-search-spinner").css("display", "none");
                }

                function showMoreSpinner() {
                $("#related-more-spinner").css("display", "inline");
                }

                function hideMoreSpinner() {
                $("#related-more-spinner").css("display", "none");
                }

        """ % dict(url=url,
                   urlSearch=self.related_url(),
                   id=self.name.replace('.', '-'),
                   folderEvent=self.folderEvent,
                   selectEvent=self.selectEvent,
                   expandSpeed=self.expandSpeed,
                   collapseSpeed=self.collapseSpeed,
                   multiFolder=str(self.multiFolder).lower(),
                   multiSelect=str(self.multi_select).lower(),
                   name=self.name,
                   klass=self.klass,
                   title=self.title,
                   perc="100%",
                   button_val=translate(
                       u'heading_contenttree_browse',
                       default=u'Browse for items',
                       domain='collective.z3cform.widgets',
                       context=self.request))
#                   button_val=_(u'browse...'))


@implementer(z3c.form.interfaces.IFieldWidget)
def MultiContentSearchFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field,
                                      MultiContentSearchWidget(request))
