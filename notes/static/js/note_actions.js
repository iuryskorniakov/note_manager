function createForm(url_){
  form = new Ext.form.FormPanel({
    baseCls: 'x-plain',
    labelWidth: 55,
    url: url_,
    layout: {
      type: 'vbox',
      align: 'stretch'
    },
    defaults: {
      xtype: 'textfield'
    },
    items: [
      {
        plugins: [ Ext.ux.FieldLabeler ],
        fieldLabel: 'title',
        dataIndex: 'title',
        name: 'title',
        displayField: false
      },
      {
        xtype: 'combo',
        store: ['Notice', 'Reference', 'Reminder', 'TODO' ],
        plugins: [Ext.ux.FieldLabeler ],
        fieldLabel: 'Category',
        dataIndex: 'category',
        name: 'category',
        disableKeyFilter: true
      },
      {
        plugins: [ Ext.ux.FieldLabeler ],
        xtype: 'checkbox',
        fieldLabel: 'Favorites',
        dataIndex: 'favorites',
        name: 'favorites'
      },
      {
        plugins: [ Ext.ux.FieldLabeler ],
        xtype: 'checkbox',
        fieldLabel: 'Publish',
        dataIndex: 'publish',
        name: 'publish'
      },
      {
        xtype: 'htmleditor',
        fieldLabel: 'text',
        hideLabel: true,
        dataIndex: 'text',
        name: 'text',
        flex: 1
      }

    ]
  });
  return form
};


function createWindow(url_){
    w = new Ext.Window({
    title: 'Compose note',
    collapsible: true,
    maximizable: true,
    width: 750,
    height: 500,
    minWidth: 300,
    minHeight: 200,
    layout: 'fit',
    plain: true,
    bodyStyle: 'padding:5px;',
    buttonAlign: 'center',
    items: form,
    buttons: [
      {
        text: "Save text",
        handler: function () {
          form.getForm().submit({
            url: url_,
            waitMsg: 'Loading data...',
            success: function (form, action) {
              Ext.getCmp('myNotes').getView().ds.reload();
              w.close()
            },
            failure: function (form, action) {
              Ext.Msg.alert('Failed', action.result.msg);
            }
          })
        }
      },
      {
        text: 'Cancel',
        handler: function () {
          w.close()
        }
      }
    ]
  });
  return w
}


function createNote(crt) {
  var url_ = '/add_note'

  var form = createForm(url_)
  var w = createWindow(url_)

  w.show();
}

$(document).on("pageload", function () {
  alert("pageload event fired!");
});

function actionWithNote(cpn, rowIndex, e) {
  var uuid = cpn.store.getAt(rowIndex).get('uuid');
  if (e.target.className.indexOf('btn-open') > -1) {
    window.open('/note' + '/' + uuid);
  }
  else if (e.target.className.indexOf('btn-edit') > -1) {
    var url_ = '/get_one_note'

    var form = createForm(url_)

    form.getForm().load({
      url: url_,
      params: {
        uuid: uuid
      },
      failure: function (form, action) {
        Ext.Msg.alert("Load failed", action.result.errorMessage);
      }
    });
    var w = createWindow('/edit_note')
    w.show();
  }
  else if (e.target.className.indexOf('btn-delete') > -1) {
    var delNote = function (btn) {
      console.info('You pressed ' + btn);
      if (btn == 'yes') {
        Ext.Ajax.request({
          url: '/delete_note',
          success: function () {
            Ext.getCmp('myNotes').getView().ds.reload();
          },
          failure: function () {
            alert('Error in server');
          },
          params: {uuid: uuid}
        });
      }
    };
    Ext.MessageBox.show({
      title: 'Delete note?',
      msg: 'You are deleting this note. Continue?',
      buttons: Ext.MessageBox.YESNO,
      fn: delNote,
      icon: Ext.MessageBox.QUESTION
    });
  }
  console.debug(e);
}


