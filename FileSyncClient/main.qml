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
