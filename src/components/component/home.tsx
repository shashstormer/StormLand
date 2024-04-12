"use client"
import Link from "next/link";
import { SearchBar } from "@/components/ui/search";
import React, { useState, useEffect } from "react";
import { api_url, AppsResponse, AppData, AppComponent } from "@/config";

export function Home() {
    const [globalDisplayId, setGlobalDisplayId] = useState("");
    const [globalAppName, setGlobalAppName] = useState("");
    const [appsList, setAppsList] = useState<AppsResponse>({"favourites": [{"name": "loading...", "display_id": "loading...", "launch_count": 0}], "app_list": [{"name": "loading...", "display_id": "loading...", "launch_count": 0}]});

  return (
    <div className="flex flex-col h-screen w-full border-t border-gray-200 dark:border-gray-800">
      <Header setAppsList={setAppsList}/>
      <MainContent setGlobalAppName={setGlobalAppName} setGlobalId={setGlobalDisplayId} appsList={appsList} setAppsList={setAppsList}/>
        {
            globalDisplayId && (<EditBox displayId={globalDisplayId} appName={globalAppName} setGlobalId={setGlobalDisplayId} setGlobalAppName={setGlobalAppName} setAppsList={setAppsList}/>)
        }
    </div>
  );
}

function Header({setAppsList}: {setAppsList: React.Dispatch<React.SetStateAction<AppsResponse>>}) {
  return (
    <header className="flex h-16 w-full items-center border-b border-gray-200 px-4 shrink-0 md:px-6 dark:border-gray-800">
      <div className="flex w-full justify-between">
        <Brand />
        <SearchBar setAppsList={setAppsList}/>
      </div>
    </header>
  );
}

function Brand() {
  return (
    <div className="flex items-center space-x-4">
      <Link href="#" className="flex items-center space-x-2 text-lg font-medium">
        <span className="text-white bold underline">StormLand</span>
      </Link>
    </div>
  );
}

function MainContent({setGlobalId, setGlobalAppName, appsList, setAppsList}:{setGlobalId: React.Dispatch<React.SetStateAction<string>>, setGlobalAppName: React.Dispatch<React.SetStateAction<string>>, appsList: AppsResponse, setAppsList: React.Dispatch<React.SetStateAction<AppsResponse>>}) {
  return (
    <div className="w-full">
      <Sections setGlobalId={setGlobalId} setGlobalAppName={setGlobalAppName} appsList={appsList} setAppsList={setAppsList}/>
    </div>
  );
}


function Sections({setGlobalId, setGlobalAppName, appsList, setAppsList}:{setGlobalId: React.Dispatch<React.SetStateAction<string>>, setGlobalAppName: React.Dispatch<React.SetStateAction<string>>, appsList: AppsResponse, setAppsList: React.Dispatch<React.SetStateAction<AppsResponse>>}) {

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${api_url}apps`);
        const data: AppsResponse = await response.json();
        setAppsList(data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData().then();
  }, [setAppsList]);

  return (
    <section className="flex items-center mt-[20px]">
      <Section width="w-2/6">
        <span>Favourites</span>
        <Apps setGlobalId={setGlobalId} setGlobalAppName={setGlobalAppName} appsList={appsList.favourites}></Apps>
      </Section>

      <Section width="w-4/6">
        <span>All Apps</span>
        <Apps setGlobalId={setGlobalId} setGlobalAppName={setGlobalAppName} appsList={appsList.app_list}></Apps>
      </Section>
    </section>
  );
}

function Section({ children, width = "full", center = true }: { children: React.ReactNode, width?: string, center?: boolean }) {
  return (
    <div className={`p-3 space-x-2 ${width} ${center ? "text-center" : ""} border-r border-l border-gray-200 dark:border-gray-800`}>
      {children}
    </div>
  );
}

function Apps({ appsList,  setGlobalId, setGlobalAppName}: { appsList: AppData[], setGlobalId: React.Dispatch<React.SetStateAction<string>>, setGlobalAppName: React.Dispatch<React.SetStateAction<string>> }) {
  return (
    <div className={"flex flex-wrap mt-2"}>
      {appsList.map((app) => (
        <App setGlobalId={setGlobalId} setGlobalAppName={setGlobalAppName} key={app.display_id} {...app} />
      ))}
    </div>
  );
}

function App({ name, display_id, setGlobalId, setGlobalAppName }: AppComponent) {
    function showEditBox() {
        setGlobalId(display_id);
        setGlobalAppName(name);
    }
  return (
      <div
          className={"w-48 h-48 m-2 relative shadow-md" +
              " shadow-rose-950"}>
          <button className="border relative rounded-md border-gray-300 dark:border-gray-700 w-48 h-48 bg-white bg-opacity-5 ml-auto mr-auto"
                  onClick={async () => {
                      await fetch(api_url + "apps/launch/" + display_id)
                  }}>
              <h3 className="text-lg font-semibold mb-3">{name}</h3>
              <img
                  className="text-sm text-gray-500 dark:text-gray-400 ml-auto mr-auto"
                  width={100}
                  height={100}
                  alt={name}
                  src={api_url + "apps/image/" + display_id}
              />
          </button>
          <div className={"absolute top-[8px] right-[3px] h-[22px] w-[22px] z-[5] hover:cursor-alias"}>
              <img
                  className="text-sm text-gray-500 dark:text-gray-400 ml-auto mr-auto"
                  width={22}
                  height={22}
                  alt={"edit icon"}
                  src={api_url + "assets/image/editicon.png"}
                  onClick={showEditBox}
              />
          </div>
      </div>
  );
}

function EditBox({ displayId, appName, setGlobalId, setGlobalAppName, setAppsList}:{displayId: string, appName: string, setGlobalId: React.Dispatch<React.SetStateAction<string>>, setGlobalAppName: React.Dispatch<React.SetStateAction<string>>, setAppsList: React.Dispatch<React.SetStateAction<AppsResponse>>}) {
    const [newName, setNewName] = useState(appName);
    async function onClose() {
        setGlobalId("");
        setGlobalAppName("");
        const response = await fetch(`${api_url}apps`);
        const data: AppsResponse = await response.json();
        setAppsList(data);
    }
    const handleDelete = async () => {
        try {
            await fetch(`${api_url}apps/remove/${displayId}`);
            await onClose();
        } catch (error) {
            console.error("Error deleting app:", error);
        }
    };

    const handleCancel = async () => {
        await onClose();
    };

    const handleConfirm = async () => {
        try {
            await fetch(`${api_url}apps/update/${displayId}?new_name=${newName}`);
            await onClose();
        } catch (error) {
            console.error("Error updating app name:", error);
        }
    };

    return (
        <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-[6]">
            <div className="bg-black bg-opacity-90 p-4 rounded-md w-96 z-[10]"
            >
                <h2 className="text-xl font-medium mb-4">Edit App Name</h2>
                <input
                    type="text"
                    className="border p-2 mb-4 w-full bg-black rounded-md"
                    value={newName}
                    onChange={(e) => setNewName(e.target.value)}
                />
                <div className="flex justify-end space-x-2">
                    <button
                        className="bg-red-500 text-white px-4 py-2 rounded-md"
                        onClick={handleDelete}
                    >
                        Delete
                    </button>
                    <button
                        className="bg-yellow-500 text-white px-4 py-2 rounded-md"
                        onClick={handleCancel}
                    >
                        Cancel
                    </button>
                    <button
                        className="bg-green-500 text-white px-4 py-2 rounded-md"
                        onClick={handleConfirm}
                    >
                        Confirm
                    </button>
                </div>
            </div>
        </div>
    );
}
