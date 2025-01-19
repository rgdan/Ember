// ==UserScript==
// @name         Ember | Flint
// @namespace    http://tampermonkey.net/
// @icon         https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/97/Flint_JE3_BE3.png/revision/latest?cb=20190430051311
// @version      2.1
// @description  First part of Ember, extracts schedule info to be used to put together a schedule.
// @author       .
// @match        https://tec-appsext.itcr.ac.cr/Matricula/frmMatricula.aspx
// @grant        GM_xmlhttpRequest
// @connect      tec-appsext.itcr.ac.cr
// ==/UserScript==

(function () {
    'use strict';

    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    const getCourseSchedule = async (courseId) => {
        const url = 'https://tec-appsext.itcr.ac.cr/Matricula/frmMatricula.aspx/ConsultaHorarios';
        const headers = { 'Content-Type': 'application/json; charset=UTF-8' };
        const body = JSON.stringify({ idMateria: courseId });

        return new Promise((resolve, reject) => {
            GM_xmlhttpRequest({
                method: 'POST',
                url: url,
                headers: headers,
                data: body,
                onload: (response) => {
                    try {
                        const data = JSON.parse(response.responseText);
                        resolve(data);
                    } catch (error) {
                        reject('Error parsing schedule data');
                    }
                },
                onerror: reject,
            });
        });
    };

    const logToConsole = (message, type = 'log') => {
        const timestamp = new Date().toLocaleTimeString();
        const consoleElement = document.getElementById('userConsole');
        const newMessage = document.createElement('div');
        const timestampStyled = `<span style="color: red;">[${timestamp}]</span> `;

        if (type === 'log') {
            newMessage.innerHTML = timestampStyled + message;
        }
        if (type === 'error') {
            newMessage.innerHTML = timestampStyled + `<span style="color: red;">${message}</span>`;
        }
        if (type === 'success') {
            newMessage.innerHTML = timestampStyled + `<span style="color: green;">${message}</span>`;
        }
        consoleElement.appendChild(newMessage);
    };

    const parseSchedule = (scheduleString) => {
        const scheduleArray = scheduleString.split(',').map(item => {
            const [day, timeRange] = item.trim().split(' ');
            const [start_time, end_time] = timeRange.split('-');
            return { day, start_time, end_time };
        });
        return scheduleArray;
    };

    const parseScheduleData = (rawJSON) => {
        try {
            const innerJSON = JSON.parse(rawJSON.d);
            const horarios = innerJSON.Horario;

            const formattedData = {};
            for (const horario of horarios) {
                const courseId = horario.IdMateria;
                const groupId = horario.IdGrupo;
                const courseName = horario.NomMateria;
                const campus = horario.Sede;
                const professors = horario.ListaProfesores.join(", ");
                const capacity = horario.Capacidad;
                const itineraries = horario.Itinerario;

                const schedule = itineraries.map(itinerary =>
                `${itinerary.Dia} ${itinerary.Inicio}-${itinerary.Fin}`
                ).join(", ");

                const parsedSchedule = parseSchedule(schedule);

                if (!formattedData[courseId]) {
                    formattedData[courseId] = {
                        course_name: courseName,
                        campuses: {}
                    };
                }

                if (!formattedData[courseId].campuses[campus]) {
                    formattedData[courseId].campuses[campus] = {};
                }

                formattedData[courseId].campuses[campus][groupId] = {
                    schedule: parsedSchedule,
 classroom: itineraries[0].Aula ? `Aula ${itineraries[0].Aula}` : "No Aula",
 professors,
 capacity
                };
            }
            return formattedData;
        } catch (error) {
            logToConsole(`Error parsing raw JSON: ${error}`, 'error');
            return null;
        }
    };

    async function extractData() {
        const tableBody = document.querySelector('#tBodyCursos');
        if (!tableBody) {
            logToConsole("Course table not found.", 'error');
            return;
        }

        const rows = tableBody.querySelectorAll('tr[id]');
        const data = {};

        for (const row of rows) {
            const courseId = row.id;
            if (courseId.startsWith("tr")) continue;

            const courseNameElement = row.querySelector('.colMateria span');
            const courseName = courseNameElement ? courseNameElement.textContent.trim() : "Unknown Course";

            data[courseId] = {
                course_name: courseName,
                campuses: {},
            };
        }

        logToConsole("Extracted basic course data.", 'success');

        for (const [courseId, courseData] of Object.entries(data)) {
            logToConsole(`Fetching schedule for course: ${courseId}`);
            try {
                await sleep(2000);
                const scheduleData = await getCourseSchedule(courseId);
                const formattedSchedule = parseScheduleData(scheduleData);
                if (formattedSchedule && formattedSchedule[courseId]) {
                    data[courseId].campuses = formattedSchedule[courseId].campuses;
                    logToConsole(`Schedule for ${courseId} fetched successfully.`, 'success');
                }
            } catch (error) {
                logToConsole(`Failed to fetch schedule for ${courseId}: ${error}`, 'error');
            }
        }

        logToConsole("All course schedules fetched and processed.", 'success');

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        downloadButton.onclick = function () {
            const a = document.createElement('a');
            a.href = url;
            a.download = 'ember_schedule_export.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        };

        downloadButton.style.backgroundColor = '#ca4e32';
        downloadButton.style.color = 'white';
        downloadButton.disabled = false;
    }

    const buttonBox = document.createElement('div');
    buttonBox.style.position = 'fixed';
    buttonBox.style.bottom = '10px';
    buttonBox.style.right = '10px';
    buttonBox.style.backgroundColor = 'rgba(184, 75, 41, 0.8)';
    buttonBox.style.border = '1px solid white';
    buttonBox.style.padding = '10px';
    buttonBox.style.zIndex = '9999';
    buttonBox.style.borderRadius = '8px';
    buttonBox.style.display = 'flex';
    buttonBox.style.flexDirection = 'column';
    buttonBox.style.alignItems = 'center';
    buttonBox.style.gap = '10px';

    const startButton = document.createElement('button');
    startButton.textContent = 'Extract Course Data';
    startButton.style.backgroundColor = '#ca4e32';
    startButton.style.border = '1px solid white';
    startButton.style.padding = '10px';
    startButton.style.color = 'white';
    startButton.style.cursor = 'pointer';
    startButton.style.borderRadius = '8px';
    startButton.addEventListener('click', extractData);
    buttonBox.appendChild(startButton);

    const downloadButton = document.createElement('button');
    downloadButton.textContent = 'Download JSON';
    downloadButton.style.backgroundColor = 'black';
    downloadButton.style.border = '1px solid white';
    downloadButton.style.padding = '10px';
    downloadButton.style.color = 'white';
    downloadButton.style.cursor = 'pointer';
    downloadButton.style.borderRadius = '8px';
    downloadButton.disabled = true;
    buttonBox.appendChild(downloadButton);

    document.body.appendChild(buttonBox);

    const consoleElement = document.createElement('div');
    consoleElement.id = 'userConsole';
    consoleElement.style.position = 'fixed';
    consoleElement.style.bottom = '10px';
    consoleElement.style.left = '10px';
    consoleElement.style.width = '87%';
    consoleElement.style.maxHeight = '150px';
    consoleElement.style.overflowY = 'auto';
    consoleElement.style.backgroundColor = 'rgba(241, 241, 241, 0.8)';
    consoleElement.style.border = '1px solid #ca4e32';
    consoleElement.style.padding = '10px';
    consoleElement.style.fontSize = '12px';
    consoleElement.style.color = '#000';
    consoleElement.style.zIndex = '9999';
    consoleElement.style.borderRadius = '8px';

    const logTitle = document.createElement('div');
    logTitle.textContent = "Ember Log";
    logTitle.style.fontWeight = 'bold';
    logTitle.style.color = '#6c483e';
    logTitle.style.fontSize = '16px';
    logTitle.style.marginBottom = '10px';
    consoleElement.appendChild(logTitle);

    document.body.appendChild(consoleElement);
})();
