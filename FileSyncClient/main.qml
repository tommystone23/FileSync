import QtQuick 6.0
import QtQuick.Window 6.0
import Controller 1.0
import QtQuick.Controls 2.6
import Qt.labs.folderlistmodel 2.6

Window {
    id: main_window
    width: 640
    height: 480
    visible: true
    title: qsTr("FileSync")
    property string file_prefix: "file://"
    Controller {
        id: controller
    }

    Item {
        id: top_bar
        anchors.top: parent.top
        width: parent.width
        height: parent.height / 6
        Button {
            id: connect_button
            text: "Connect"
            onClicked: {
                dialog.open()
            }
        }
        Dialog {
            id: dialog
            title: "Connect To Server"
            modal: true
            property int content_height: height / 8
            standardButtons: Dialog.Ok | Dialog.Cancel
            width: main_window.width / 2
            height: main_window.height / 2
            x: (main_window.width - width) / 2
            y: (main_window.height - height) / 2
            Text {
                id: device_text
                text: "Device IP:"
                height: dialog.content_height
                width: dialog.width / 2
                verticalAlignment: Text.AlignVCenter
                leftPadding: dialog.width / 4
            }
            TextField {
                id: device_input
                placeholderText: "Device IP..."
                width: dialog.width / 2
                height: dialog.content_height
                anchors.right: parent.right
            }
            Text {
                id: username_text
                text: "Username:"
                height: dialog.content_height
                width: dialog.width / 2
                verticalAlignment: Text.AlignVCenter
                leftPadding: dialog.width / 4
                anchors.top: device_text.bottom
            }
            TextField {
                id: username_input
                placeholderText: "Username..."
                width: dialog.width / 2
                height: dialog.content_height
                anchors.right: parent.right
                anchors.top: device_input.bottom
            }
            Text {
                id: password_text
                text: "Password:"
                height: dialog.content_height
                width: dialog.width / 2
                verticalAlignment: Text.AlignVCenter
                leftPadding: dialog.width / 4
                anchors.top: username_text.bottom
            }
            TextField {
                id: password_input
                placeholderText: "Password..."
                width: dialog.width / 2
                height: dialog.content_height
                anchors.right: parent.right
                echoMode: TextInput.Password
                anchors.top: username_input.bottom
            }
            onAccepted: {
                var host = device_input.text
                var username = username_input.text
                var password = password_input.text
                controller.connect_host(host, username, password)
            }
        }
    }

    Item {
        id: left_column
        anchors {
            left: parent.left
            bottom: parent.bottom
            top: top_bar.bottom
        }
        width: parent.width / 2

        ListView {
            id: folder_view
            anchors.fill: parent
            FileListModel {
                id: folder_model
                folder: file_prefix + "/home/tommy/"
                showDirs: true
                showDotAndDotDot: true
                nameFilters: ["*"]
                sortField :  "Name"
            }
            Component {
                id: file_delegate
                Button {
                    id: dir_button
                    text: fileName
                    width: parent.width
                    onClicked: {
                        if(folder_model.isFolder(index))
                            folder_model.folder = file_prefix + folder_model.get(index, "filePath")

                    }
                }
            }
            model: folder_model
            delegate: file_delegate
        }
    }
}
