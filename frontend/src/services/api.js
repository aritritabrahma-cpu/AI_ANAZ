const API_URL = "http://127.0.0.1:8000/api/latest";

export async function fetchApiData() {

    try {

        const response = await fetch(API_URL);

        if (!response.ok)
            throw new Error("Backend not reachable");

        return await response.json();

    }

    catch (err) {

        console.error(err);

        return [];

    }

}