import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button";
import {api_url, AppsResponse} from "@/config";
import React, {useState} from "react";

export function SearchBar({ setAppsList }: {setAppsList: React.Dispatch<React.SetStateAction<AppsResponse>>}) {
  return (
    <div className="flex items-center space-x-4">
        <SearchInput />
        <SearchButton />
        <PlusButton setAppsList={setAppsList}/>
        <AddWebsite setAppsList={setAppsList}/>
    </div>
  );
}

function AddWebsite({setAppsList}: {setAppsList: React.Dispatch<React.SetStateAction<AppsResponse>>}) {
    const [addSiteMenu, setAddSiteMenu] = useState(false);
    const [siteName, setSiteName] = useState("");
    const [siteUrl, setSiteUrl] = useState("");

  return (
    <div className={"flex"} onClick={()=>{setAddSiteMenu(true)}}>
      <Button type={"submit"}>Add Site</Button>
        {addSiteMenu && (<AddSiteMenu siteName={siteName} siteUrl={siteUrl} setSiteName={setSiteName} setSiteUrl={setSiteUrl} setAppsList={setAppsList} setAddSiteMenu={setAddSiteMenu}/>)}
    </div>
  );
}

function AddSiteMenu({siteName, siteUrl, setSiteName, setSiteUrl, setAppsList, setAddSiteMenu}: {siteName: string, siteUrl: string, setSiteName: React.Dispatch<React.SetStateAction<string>>, setSiteUrl: React.Dispatch<React.SetStateAction<string>>, setAppsList: React.Dispatch<React.SetStateAction<AppsResponse>>, setAddSiteMenu: React.Dispatch<React.SetStateAction<boolean>>}) {
        async function onClose() {
        const response = await fetch(`${api_url}apps`);
        const data: AppsResponse = await response.json();
        setAppsList(data);
        setAddSiteMenu(false);
    }


    const handleCancel = async () => {
        await onClose();
    };

    const handleConfirm = async () => {
        try {
            await fetch(`${api_url}apps/addsite?name=${siteName}&url=${siteUrl}`);
            await onClose();
        } catch (error) {
            console.error("Error adding website:", error);
        }
    };

    return (
        <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-[6]">
            <div className="bg-black bg-opacity-90 p-4 rounded-md w-96 z-[10]"
            >
                <h2 className="text-xl font-medium mb-4">Add Website</h2>
                <input
                    type="text"
                    className="border p-2 mb-4 w-full bg-black rounded-md"
                    value={siteName}
                    placeholder={"name"}
                    onChange={(e) => setSiteName(e.target.value)}
                />
                <input
                    type="text"
                    className="border p-2 mb-4 w-full bg-black rounded-md"
                    value={siteUrl}
                    placeholder={"URL"}
                    onChange={(e) => setSiteUrl(e.target.value)}
                />
                <div className="flex justify-end space-x-2">
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

function SearchInput() {
  return (
    <div className="relative w-full capitalize">
      <SearchIcon className="absolute inset-y-1.5 inset-x-2.5 my-1.5 left-2.5 w-4 h-4 text-gray-500 dark:text-gray-400" />
      <Input className="border-0 shadow-none appearance-none pl-8" placeholder="Search" type="search" />
    </div>
  );
}

function SearchButton() {
  return (
    <Button size="icon" type="submit">
      <SearchIcon className="w-8 h-4" />
      <span className="sr-only">Search</span>
    </Button>
  );
}

function PlusButton({setAppsList}: {setAppsList: React.Dispatch<React.SetStateAction<AppsResponse>>}) {
    async function fetchLaunchAppAdder() {
        await fetch(api_url+"apps/add");
        const response = await fetch(`${api_url}apps`);
        const data: AppsResponse = await response.json();
        setAppsList(data);
    }
  return (
    <Button size="icon" type="submit" onClick={fetchLaunchAppAdder}>
      <PlusIcon className="w-8 h-4" />
      <span className="sr-only">Add App</span>
    </Button>
  );
}


function SearchIcon(props: {className: string}) {
    return (
        <svg
            {...props}
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.3-4.3" />
        </svg>
    );
}

function PlusIcon(props: { className: string }) {
    return (
        <svg
            {...props}
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
    );
}
