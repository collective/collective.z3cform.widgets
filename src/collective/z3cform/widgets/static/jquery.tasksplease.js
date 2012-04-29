(function($) {
    /**
     *  @constructor
     *  @param jqElement item, The textarea element
     *  @param {Object} conf, the conf dictionary
     */
    function TasksPlease(item, conf){
        var self = this,
            sorteable = conf.sorteable,
            taskmanager;

        $.extend(self, {
            init: function(){
                self.setup();
            },

            /*
             * on demand task creation, by default is going to create the task
             * like the latest element, but the order can be setted using an index.
             * @param text, just text for the task
             * @param position, and index value indicating the position, 0 is first, -1 is last.
             * @return task, the dom task element
             */
            create_task: function(text, position){
                if (position === undefined) {
                    position = -1;
                }
                var task = $('<li/>');
                task.text(text);

                task.append('<a class="remove" href="#"><span>'+tp_i18n.delete_task+'</span></a>');
                self.delete_event(task.find('.remove'), task);
                taskmanager.append(task);

                return task;
            },

            /*
             * Delete the task in the indicated index
             * @param index, index of the objective task to delete in the textarea
             */
            delete_task: function(index) {
                //remove the li element
                element_to_delete = taskmanager.find('li')[index];
                if ( element_to_delete !== undefined ) {
                    $(element_to_delete).remove();

                    //create and array and remove the deleted object from the
                    //text area
                    var text_area_list = item.val().split('\n');
                    text_area_list.splice(index, 1);

                    //then, recreate the data again.
                    item.val(text_area_list.join('\n'));
                }
            },
            /*
             * creates all the basic structure for the tasks, if a textarea has
             * values, is going to recreate those like tasks
             */
            setup: function(){
                var lines = [];
                taskmanager = $('<ul class="tasksplease"/>');

                //check textarea content
                var value = item.val();
                if (value[0] !== undefined) {
                    lines = value.split('\n');
                }

                //lets recreate the textarea in the form of tasks
                $.each(lines, function(i, e){
                    self.create_task(e, i);
                });

                //widget container
                self.container = $('<div class="tasksplease-container"/>');
                //lets create the "add new" task textarea
                var add_new = $('<textarea type="text" name="task-description" \
                    class="task-description" rows="1" placeholder="'+tp_i18n.add_task+'"></textarea>');

                self.container.append(taskmanager)
                              .append(add_new)
                              .append('<input class="add_task" type="submit" value="'+tp_i18n.add+'"/>');
                item.after(self.container);

                self.add_new_event(self.container.find('.add_task'));
                item.hide();
            },

            add_new_event: function(trigger){

                $(trigger).click(function(e){
                    var description = $(this).siblings('.task-description');
                    var value = description.val();
                    //only add the descrition if is not empty
                    if (value[0] !== undefined) {
                        //replace new lines per spaces =)
                        var clean_text = value.replace(/(\r\n|\n|\r)/gm," ");

                        self.create_task(clean_text);

                        description_content = item.val() + '\n' + clean_text;
                        if (item.val()[0] === undefined) {
                            description_content = clean_text;
                        }

                        item.val(description_content)
                        //after creation we NEED to delete the content of the
                        //task description field, just for usability
                        description.val('');
                    }
                    e.preventDefault()
                });
            },

            delete_event: function(trigger, element_to_delete){
                $(trigger).click(function(e){
                    var index = $(element_to_delete).index();
                    self.delete_task(index);

                    e.preventDefault();
                });
            },

            edit_event: function(trigger, element_to_edit) {
                $(trigger).click(function(e){
                    e.preventDefault();
                });
            }
        });

        self.init();
    };

    $.fn.tasksplease = function(options) {

        // already instanced, return the data object
        var el = this.data("tasksplease");
        if (el) { return el; }

        //default settings
        var settings = {
            'sorteable': true //allow sorting?
        }

        if (options) {
            $.extend(settings, options);
        }

        return this.each(function() {
            el = new TasksPlease($(this), settings);
            $(this).data("tasksplease", el);
        });

    };
})(jQuery);
