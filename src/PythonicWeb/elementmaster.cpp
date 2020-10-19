/*
 * This file is part of Pythonic.

 * Pythonic is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.

 * Pythonic is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with Pythonic. If not, see <https://www.gnu.org/licenses/>
 */

#include "elementmaster.h"




ElementMaster::ElementMaster(bool socket,
                             bool plug,
                             QUrl pixMapPath,
                             QString objectName,
                             bool iconBar,
                             QWidget *parent)
    : QWidget(parent)
    , m_symbol(pixMapPath, LABEL_SIZE, this)
{

    setAttribute(Qt::WA_DeleteOnClose);

    m_id = QRandomGenerator::global()->generate();
    QString widgetName = QStringLiteral("%1 - 0x%2").arg(objectName).arg(m_id, 8, 16);
    setObjectName(widgetName);
    qCDebug(logC, "called - %s added", widgetName.toStdString().c_str());
    m_layout.setContentsMargins(10, 0, 30, 0);
    m_innerWidgetLayout.setContentsMargins(0, 5, 0, 5);

    /* Enable / disable socket/plug */

    m_socket.setVisible(socket);
    m_plug.setVisible(plug);

    /* Enable / disable iconbar of element */

    m_iconBar.setVisible(iconBar);

    /* m_symbol needs object name to apply stylesheet */

    m_symbol.setObjectName("element");

    /* Setup symbol widget */
    m_symbolWidget.setLayout(&m_symbolWidgetLayout);
    m_symbolWidgetLayout.addWidget(&m_socket);
    m_symbolWidgetLayout.addWidget(&m_symbol);
    m_symbolWidgetLayout.addWidget(&m_plug);

    /* Defualt name = object name */

    m_labelText.setText(widgetName);


    //resize(200, 200);
    /* Setup inner widget: symbolWidget and text-label */

    m_innerWidget.setLayout(&m_innerWidgetLayout);
    m_innerWidgetLayout.setSizeConstraint(QLayout::SetFixedSize);

    m_innerWidgetLayout.addWidget(&m_labelText);
    m_innerWidgetLayout.addWidget(&m_symbolWidget);


    m_layout.addWidget(&m_innerWidget);
    m_layout.addWidget(&m_iconBar);

    m_layout.setSizeConstraint(QLayout::SetFixedSize);
    //setSizePolicy(m_sizePolicy);
    setLayout(&m_layout);
    //startHighlight();
    stopHighlight();



    /* Signals and Slots */
    connect(&m_iconBar.m_deleteBtn, &QPushButton::clicked,
            this, &ElementMaster::deleteSelf);

}

void ElementMaster::startHighlight()
{
    qCDebug(logC, "called");
    m_symbol.setStyleSheet("#element { background-color: #636363;\
                  border: 3px solid #fce96f; border-radius: 20px; }");
}

void ElementMaster::stopHighlight()
{
    qCDebug(logC, "called");
    m_symbol.setStyleSheet("#element { background-color: #636363;\
                           border: 3px solid #ff5900; border-radius: 20px; }");
}

bool ElementMaster::getDebugState() const
{
    return m_iconBar.m_debugBtn.isChecked();
}

void ElementMaster::deleteSelf()
{
    qCInfo(logC, "called %s", objectName().toStdString().c_str());
    emit remove(this);
}

void ElementMaster::moveEvent(QMoveEvent *event)
{
    // Linien neu malen
    //qCInfo(logC, "called");
}


/*****************************************************
 *                                                   *
 *                       PLUG                        *
 *                                                   *
 *****************************************************/

void ElementPlug::enterEvent(QEvent *event)
{
    qCInfo(logC, "called");
    setStyleSheet("background-color: gold;");
}

void ElementPlug::leaveEvent(QEvent *event)
{
    qCInfo(logC, "called");
    setStyleSheet("background-color: transparent;");
}



/*****************************************************
 *                                                   *
 *                      SOCKET                       *
 *                                                   *
 *****************************************************/

void ElementSocket::enterEvent(QEvent *event)
{
    qCInfo(logC, "called");
    setStyleSheet("background-color: chartreuse;");
}

void ElementSocket::leaveEvent(QEvent *event)
{
    qCInfo(logC, "called");
    setStyleSheet("background-color: transparent;");
}